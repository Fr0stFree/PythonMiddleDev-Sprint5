from elasticsearch import AsyncElasticsearch

from core.mixins import Singleton


class ElasticApp(Singleton):
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self._es: AsyncElasticsearch | None = None

    async def connect(self) -> None:
        self._es = AsyncElasticsearch(f"http://{self._host}:{self._port}")
        await self._es.ping()

    async def disconnect(self) -> None:
        await self._es.close()
