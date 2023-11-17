import datetime as dt
from abc import ABC, abstractmethod
from typing import Optional, Self, Type
from uuid import UUID

import orjson
from db.elastic import AsyncSearchEngine
from db.redis import CacheApp
from fastapi import Request
from pydantic import BaseModel

from core.mixins import Singleton


class BaseService(Singleton, ABC):
    def __init__(
        self,
        cache_app: CacheApp,
        search_engine: AsyncSearchEngine,
    ) -> None:
        self.cache_app = cache_app
        self.search_engine = search_engine

    @classmethod
    def get_instance(cls, request: Request) -> Self:
        """Create an instance automatically if not exist."""
        if cls._instance is None:
            cls._instance = cls(cache_app=request.app.state.cache_app,
                                search_engine=request.app.state.search_engine)
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

    @property
    def model_class_name(self) -> str:
        return self.model_class.__name__.lower()

    async def get_by_id(self, id: UUID) -> Optional[model_class]:
        model = await self.cache_app.get_one(id, self.model_class_name)
        if model:
            return self.model_class.model_validate_json(model)

        model = await self.search_engine.get_one(str(id), self.elastic_index)
        if model:
            model = self.model_class.model_validate(model)
            await self.cache_app.set_one(model.id, model.model_dump_json(), self.model_class_name, self.cache_expires)
            return model

        return None

    async def get_many(self, query: dict, params: dict) -> list[model_class]:
        models = await self.cache_app.get_many(query, params, self.model_class_name)
        if models:
            return [self.model_class.model_validate(orjson.loads(model)) for model in models]

        models = await self.search_engine.get_many(query, params, self.elastic_index)
        if models:
            models = [self.model_class.model_validate(model) for model in models]
            await self.cache_app.set_many(query, params, [model.model_dump_json() for model in models],
                                          self.model_class_name, self.cache_expires)
            return models
        return []
