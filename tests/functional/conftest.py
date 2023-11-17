import json
from unittest.mock import Mock

import aiohttp
import pytest
import pytest_asyncio
from db.elastic import ElasticApp
from db.redis import RedisApp
from tests.functional.settings import TestSettings
from tests.functional.src.factories import FilmFactory, GenreFactory, PersonFactory
from tests.functional.testdata.es_mapping import es_mappings
from redis.asyncio import Redis

from services import FilmService, GenreService, PersonService


@pytest.fixture(scope="session")
def settings():
    return TestSettings()


@pytest_asyncio.fixture(scope="function")
async def es_client(settings):
    _search_engine = Mock(wraps=ElasticApp(host=settings.elastic_host, port=settings.elastic_port))
    await _search_engine.connect()
    yield _search_engine
    await _search_engine.disconnect()


@pytest_asyncio.fixture(scope="function")
async def redis_client(settings):
    _cache_app = Mock(wraps=RedisApp(host=settings.redis_host, port=settings.redis_port))
    await _cache_app.connect()
    yield _cache_app
    await _cache_app.disconnect()


@pytest.fixture(scope="function")
def genre_service(settings, redis_client, es_client):
    return GenreService(cache_app=redis_client, search_engine=es_client)


@pytest.fixture(scope="function")
def genre(settings):
    return GenreFactory.create()


@pytest.fixture(scope="function")
def genres(settings):
    return [GenreFactory.create() for _ in range(10)]


@pytest.fixture(scope="function")
def film_service(settings, redis_client, es_client):
    return FilmService(cache_app=redis_client, search_engine=es_client)


@pytest.fixture(scope="function")
def film(settings):
    return FilmFactory.create()


@pytest.fixture(scope="function")
def films(settings):
    return [FilmFactory.create() for _ in range(10)]


@pytest.fixture(scope="function")
def person_service(settings, redis_client, es_client):
    return PersonService(cache_app=redis_client, search_engine=es_client)


@pytest.fixture(scope="function")
def person(settings):
    return PersonFactory.create()


@pytest.fixture(scope="function")
def persons(settings):
    return [PersonFactory.create() for _ in range(10)]


@pytest_asyncio.fixture(scope="function")
async def es_write_data(es_client):
    client = es_client.instance

    async def inner(data, index):
        bulk_query = _get_es_bulk_query(data, index, "id")
        str_query = "\n".join(bulk_query) + "\n"
        await es_client.indices.delete(index=index, allow_no_indices=True, ignore_unavailable=True)
        await es_client.indices.create(index=index, mappings=es_mappings[index])

        response = await es_client.bulk(operations=str_query, refresh=True)
        if response["errors"]:
            raise Exception("Ошибка записи данных в Elasticsearch")

    yield inner

    await client.options(ignore_status=[400, 404]).delete_by_query(
        index="*", body={"query": {"match_all": {}}}, refresh=True
    )


@pytest_asyncio.fixture(scope="function")
async def redis_write_data(redis_client):
    client = redis_client.instance

    async def inner(key, data):
        return await client.set(key, data)

    yield inner

    await client.flushall()


@pytest.fixture
def make_get_request(settings):
    async def inner(query_data: dict, endpoint: str):
        url = f"http://{settings.app_host}:{settings.app_port}/api/v1/{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=query_data) as response:
                body = await response.json()
                return {"body": body, "status": response.status, "headers": response.headers}

    return inner


def _get_es_bulk_query(es_data, es_index, es_id_field) -> list:
    bulk_query = []
    for row in es_data:
        bulk_query.extend([json.dumps({"index": {"_index": es_index, "_id": row[es_id_field]}}), json.dumps(row)])
    return bulk_query
