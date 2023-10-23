from typing import Self

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis

from core.mixins import Singleton
from db import ElasticApp, RedisApp


class ServiceMixin(Singleton):
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
