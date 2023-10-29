import asyncio
import datetime as dt
import json
from abc import ABC, abstractmethod
from hashlib import md5
from typing import Optional, Self, Type
from uuid import UUID

import orjson
from elasticsearch import AsyncElasticsearch, NotFoundError
from pydantic import BaseModel
from redis.asyncio import Redis

from core.mixins import Singleton
from db import ElasticApp, RedisApp


class BaseService(Singleton, ABC):
    def __init__(
        self,
        redis: Redis,
        elastic: AsyncElasticsearch,
    ) -> None:
        self.redis = redis
        self.elastic = elastic

    @classmethod
    def get_instance(cls) -> Self:
        """Create an instance automatically if not exist."""
        if cls._instance is None:
            cls._instance = cls(redis=RedisApp.get_instance(), elastic=ElasticApp.get_instance())
        return cls._instance

    @property
    @abstractmethod
    def model_class(self) -> Type[BaseModel]:
        pass

    @property
    @abstractmethod
    def elastic_index(self) -> str:
        pass

    @property
    @abstractmethod
    def cache_expires(self) -> dt.timedelta:
        pass

    async def get_by_id(self, id: UUID) -> Optional[model_class]:
        # if (model := await self._get_cached_model(id)) is not None:
        #     return model

        if (model := await self._get_model(id)) is not None:
            asyncio.create_task(self._cache_model(model))
            return model

    async def _get_cached_model(self, id: UUID) -> Optional[model_class]:
        key = self._build_single_model_cache_key(id)
        if (model := await self.redis.get(key)) is not None:
            return self.model_class.model_validate(orjson.loads(model))

    async def _cache_model(self, model: model_class) -> None:
        key = self._build_single_model_cache_key(model.id)
        await self.redis.set(key, model.model_dump_json(), self.cache_expires)

    async def _get_model(self, id: UUID) -> Optional[model_class]:
        try:
            doc = await self.elastic.get(index=self.elastic_index, id=str(id))
            return self.model_class.model_validate(doc["_source"])
        except NotFoundError:
            return None

    async def get_many(self, query: dict, params: dict) -> list[model_class]:
        # if (models := await self._get_cached_models(query, params)) is not None:
        #     return models

        if (models := await self._get_models(query, params)) is not None:
            asyncio.create_task(self._cache_models(models, query, params))
            return models

    async def _get_cached_models(self, query: dict, params: dict) -> list[model_class] | None:
        key = self._build_many_models_cache_key(query, params)
        if not await self.redis.exists(key):
            return None

        models = await self.redis.lrange(key, 0, -1)
        return [self.model_class.model_validate(orjson.loads(model)) for model in models]

    async def _cache_models(self, models: list[model_class], query=None, params=None) -> None:
        if not models:  # no need to cache empty list
            return

        key = self._build_many_models_cache_key(query, params)
        await self.redis.lpush(key, *[model.model_dump_json() for model in models])
        await self.redis.expire(key, self.cache_expires)

    async def _get_models(self, query: dict, params: dict) -> list[model_class]:
        docs = await self.elastic.search(index=self.elastic_index, query=query, params=params)
        return [self.model_class.model_validate(doc["_source"]) for doc in docs["hits"]["hits"]]

    def _build_single_model_cache_key(self, id: UUID) -> str:
        return f"{self.model_class.__name__.lower()}#{id}"

    def _build_many_models_cache_key(self, query: dict = None, params: dict = None) -> str:
        query = query or {}
        params = params or {}
        hashed_request = md5((json.dumps(query) + str(json.dumps(params))).encode(), usedforsecurity=False).hexdigest()
        return f"{self.model_class.__name__.lower()}s#{hashed_request}"
