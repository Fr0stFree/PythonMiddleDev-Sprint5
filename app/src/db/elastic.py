from abc import ABC, abstractmethod
from logging import getLogger

from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch.exceptions import ConnectionError

from core.mixins import Singleton

logger = getLogger(__name__)


class AsyncSearchEngine(ABC):
    def __init__(self, host: str, port: int) -> None:
        self._connection_url = f"http://{host}:{port}"
        self.client = None

    @abstractmethod
    async def connect(self) -> None:
        """Connect to search engine client"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from search engine client"""
        pass

    @abstractmethod
    async def get_one(self, id: str, index: str):
        """Get model data from search engine"""
        pass

    @abstractmethod
    async def get_many(self, query: dict, params: dict, index: str):
        """Get models data from search engine"""
        pass


class ElasticApp(Singleton, AsyncSearchEngine):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def connect(self) -> None:
        logger.info(f"Connecting to elastic search on {self._connection_url}...")
        self.client = AsyncElasticsearch(self._connection_url)
        if not await self.client.ping():
            await self.client.close()
            raise ConnectionError(message=f"Cannot connect to Elastic {self._connection_url}")
        logger.info("Connected successfully.")

    async def disconnect(self) -> None:
        logger.info("Closing connection to elastic search...")
        await self.client.close()
        self.client = None
        logger.info("Connection closed successfully.")

    @property
    def instance(self) -> AsyncElasticsearch:
        if self.client is None:
            raise RuntimeError("Elastic search is not initialized.")
        return self.client

    async def get_one(self, id: str, index: str):
        try:
            doc = await self.client.get(index=index, id=id)
            return doc["_source"]
        except NotFoundError:
            return None

    async def get_many(self, query: dict, params: dict, index: str):
        docs = await self.client.search(index=index, query=query, params=params)
        return [doc["_source"] for doc in docs["hits"]["hits"]]
