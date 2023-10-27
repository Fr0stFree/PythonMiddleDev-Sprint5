import datetime as dt
from abc import ABC, abstractmethod
from typing import Optional, Self, Type
from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from pydantic import BaseModel
from redis.asyncio import Redis

from core.mixins import Singleton
from db import ElasticApp, RedisApp


class BaseService(Singleton, ABC):
    def __init__(
        self,
        redis: Redis = Depends(RedisApp.get_instance),
        elastic: AsyncElasticsearch = Depends(ElasticApp.get_instance),
    ) -> None:
        self.redis = redis
        self.elastic = elastic

    @classmethod
    def get_instance(cls) -> Self:
        """Create an instance automatically if not exist."""
        if cls._instance is None:
            cls._instance = cls()
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

    async def get_by_id(self, uuid: UUID) -> Optional[model_class]:
        if (model := await self._get_cached_model(uuid)) is not None:
            return model

        if (model := await self._get_model(uuid)) is not None:
            await self._cache_model(model)
            return model

    async def _get_cached_model(self, id: UUID) -> Optional[model_class]:
        key = f"{self.model_class.__name__.lower()}#{id}"
        if (model := await self.redis.get(key)) is not None:
            return self.model_class.model_validate(model)

    async def _cache_model(self, model: model_class) -> None:
        key = f"{self.model_class.__name__.lower()}#{model.uuid}"
        await self.redis.set(key, model.model_dump_json(), self.cache_expires)

    async def _get_model(self, id: UUID) -> Optional[model_class]:
        try:
            doc = await self.elastic.get(index=self.elastic_index, uuid=id)
            return self.model_class(**doc["_source"])
        except NotFoundError:
            return None

    async def get_many(self, *args, **kwargs) -> list[model_class]:
        pass
