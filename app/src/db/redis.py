from abc import ABC, abstractmethod
import datetime as dt
from logging import getLogger
from hashlib import md5
from uuid import UUID

import orjson
from redis.asyncio import Redis

from core.mixins import Singleton

logger = getLogger(__name__)


class CacheApp(ABC):
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self.client = None

    @abstractmethod
    async def connect(self) -> None:
        """Connect to cache app client"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from cache app client"""
        pass

    @abstractmethod
    async def get_one(self, id: UUID, model_name: str):
        """Get model data from cache"""
        pass

    @abstractmethod
    async def set_one(self, id: UUID, data: str, model_name: str, cache_expires: dt.timedelta):
        """Set model data to cache"""
        pass

    @abstractmethod
    async def get_many(self, query: dict, params: dict, model_name: str):
        """Get models data from cache"""
        pass

    @abstractmethod
    async def set_many(self, query: dict, params: dict, data: list, model_name: str, cache_expires: dt.timedelta):
        """Set models data to cache"""
        pass

    @staticmethod
    def _build_single_model_cache_key(id: UUID, model_name: str) -> str:
        """Build single model cache key"""
        return f"{model_name}#{id}"

    @staticmethod
    def _build_many_models_cache_key(query: dict = None, params: dict = None, model_name: str = '') -> str:
        """Build models cache key"""
        query = query or {}
        params = params or {}
        hashed_request = md5((orjson.dumps(query) + orjson.dumps(params)), usedforsecurity=False).hexdigest()
        return f"{model_name}s#{hashed_request}"


class RedisApp(Singleton, CacheApp):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def connect(self) -> None:
        logger.info(f"Connecting to redis on {self._host}:{self._port}...")
        self.client = Redis(host=self._host, port=self._port)
        await self.client.ping()
        logger.info("Connected successfully.")

    async def disconnect(self) -> None:
        logger.info("Closing connection to redis...")
        await self.client.close()
        self.client = None
        logger.info("Connection closed successfully.")

    @property
    def instance(self) -> Redis:
        if self.client is None:
            raise RuntimeError("Redis is not initialized.")
        return self.client

    async def get_one(self, id: UUID, model_name):
        key = self._build_single_model_cache_key(id, model_name)
        if (model := await self.client.get(key)) is not None:
            return model

    async def set_one(self, id: UUID, data: str, model_name: str, cache_expires: dt.timedelta):
        key = self._build_single_model_cache_key(id, model_name)
        await self.client.set(key, data, cache_expires)

    async def get_many(self, query: dict, params: dict, model_name):
        key = self._build_many_models_cache_key(query, params, model_name)
        if not await self.client.exists(key):
            return None
        return await self.client.lrange(key, 0, -1)

    async def set_many(self, query: dict, params: dict, data: list, model_name: str, cache_expires: dt.timedelta):
        key = self._build_many_models_cache_key(query, params, model_name)
        await self.client.lpush(key, *data)
        await self.client.expire(key, cache_expires)
