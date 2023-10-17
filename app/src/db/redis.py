from redis.asyncio import Redis

from core.mixins import Singleton


class RedisApp(Singleton):
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self._redis: Redis | None = None

    async def connect(self) -> None:
        self._redis = Redis(host=self._host, port=self._port)
        await self._redis.ping()

    async def disconnect(self) -> None:
        await self._redis.close()
