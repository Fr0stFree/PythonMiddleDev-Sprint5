from logging import getLogger

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import ConnectionError

from core.mixins import Singleton

logger = getLogger(__name__)


class ElasticApp(Singleton):
    def __init__(self, host: str, port: int) -> None:
        self._connection_url = f"http://{host}:{port}"
        self._es: AsyncElasticsearch | None = None

    async def connect(self) -> None:
        logger.info(f"Connecting to elastic search on {self._connection_url}...")
        self._es = AsyncElasticsearch(self._connection_url)
        if not await self._es.ping():
            await self._es.close()
            raise ConnectionError(message=f"Cannot connect to Elastic {self._connection_url}")
        logger.info("Connected successfully.")

    async def disconnect(self) -> None:
        logger.info("Closing connection to elastic search...")
        await self._es.close()
        self._es = None
        logger.info("Connection closed successfully.")

    @property
    def instance(self) -> AsyncElasticsearch:
        if self._es is None:
            raise RuntimeError("Elastic search is not initialized.")
        return self._es
