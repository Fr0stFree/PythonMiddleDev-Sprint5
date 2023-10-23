from unittest.mock import AsyncMock, Mock

import pytest
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from films.services import FilmService


class RedisMock(Mock):
    def __init__(self, *args, **kwargs):
        super().__init__(spec_set=Redis, *args, **kwargs)
        self.get = AsyncMock()
        self.set = AsyncMock()


class ElasticsearchMock(Mock):
    def __init__(self, *args, **kwargs):
        super().__init__(spec_set=AsyncElasticsearch, *args, **kwargs)
        self.get = AsyncMock()


@pytest.fixture(autouse=True)
def film_service():
    return FilmService(redis=RedisMock(), elastic=ElasticsearchMock())
