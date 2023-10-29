from logging import getLogger
from typing import Self

from elasticsearch import AsyncElasticsearch

from core.mixins import Singleton

logger = getLogger(__name__)


class ElasticApp(Singleton):
    def __init__(self, host: str, port: int) -> None:
        self._connection_url = f"http://{host}:{port}"
        self._es: AsyncElasticsearch | None = None

    async def connect(self) -> None:
        logger.info(f"Connecting to elastic search on {self._connection_url}...")
        self._es = AsyncElasticsearch(self._connection_url)
        await self._es.ping()
        logger.info("Connected successfully.")

    async def disconnect(self) -> None:
        logger.info("Closing connection to elastic search...")
        await self._es.close()
        self._es = None
        logger.info("Connection closed successfully.")

    @classmethod
    def get_instance(cls) -> AsyncElasticsearch:
        instance: Self = super().get_instance()
        if instance._es is None:
            raise RuntimeError("Elastic Search connection is closed")
        return instance._es
