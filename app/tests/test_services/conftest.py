from unittest.mock import AsyncMock, Mock

import pytest
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from services import FilmService, GenreService, PersonService


class RedisMock(Mock):
    def __init__(self, *args, **kwargs):
        super().__init__(spec_set=Redis, *args, **kwargs)
        self.get = AsyncMock()
        self.set = AsyncMock()
        self.exists = AsyncMock()
        self.lrange = AsyncMock()


class ElasticsearchMock(Mock):
    def __init__(self, *args, **kwargs):
        super().__init__(spec_set=AsyncElasticsearch, *args, **kwargs)
        self.get = AsyncMock()
        self.search = AsyncMock()


@pytest.fixture(autouse=True)
def film_service():
    return FilmService(redis=RedisMock(), elastic=ElasticsearchMock())


@pytest.fixture(autouse=True)
def genre_service():
    return GenreService(redis=RedisMock(), elastic=ElasticsearchMock())


@pytest.fixture(autouse=True)
def person_service():
    return PersonService(redis=RedisMock(), elastic=ElasticsearchMock())
