from logging import getLogger
from typing import Self

from redis.asyncio import Redis

from core.mixins import Singleton

logger = getLogger(__name__)


class RedisApp(Singleton):
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self._redis: Redis | None = None

    async def connect(self) -> None:
        logger.info(f"Connecting to redis on {self._host}:{self._port}...")
        self._redis = Redis(host=self._host, port=self._port)
        await self._redis.ping()
        logger.info("Connected successfully.")

    async def disconnect(self) -> None:
        logger.info("Closing connection to redis...")
        await self._redis.close()
        self._redis = None
        logger.info("Connection closed successfully.")

    @classmethod
    def get_instance(cls) -> Redis:
        instance: Self = super().get_instance()
        if instance._redis is None:
            raise RuntimeError("Redis connection is closed")
        return instance._redis
