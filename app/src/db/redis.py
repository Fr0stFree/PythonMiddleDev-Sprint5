from logging import getLogger

from redis.asyncio import Redis

from core.mixins import Singleton

logger = getLogger(__name__)


class RedisApp(Singleton):
    def __init__(self, host: str, port: int, **kwargs) -> None:
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

    @property
    def instance(self) -> Redis:
        if self._redis is None:
            raise RuntimeError("Redis is not initialized.")
        return self._redis
