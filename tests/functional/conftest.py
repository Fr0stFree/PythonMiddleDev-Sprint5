import json
from unittest.mock import Mock

import aiohttp
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from tests.functional.settings import TestSettings
from tests.functional.testdata.es_mapping import es_mappings
from redis.asyncio import Redis

from services import FilmService, GenreService, PersonService


@pytest.fixture(scope="session")
def settings():
    return TestSettings()


@pytest_asyncio.fixture(scope="function")
async def es_client(settings):
    client = Mock(wraps=AsyncElasticsearch(hosts=f"http://{settings.elastic_host}:{settings.elastic_port}"))
    yield client
    await client.close()


@pytest_asyncio.fixture(scope="function")
async def redis_client(settings):
    client = Mock(wraps=Redis(host=settings.redis_host, port=settings.redis_port))
    yield client
    await client.close()


@pytest.fixture(scope="function")
def genre_service(settings, redis_client, es_client):
    return GenreService(redis=redis_client, elastic=es_client)


@pytest.fixture(scope="function")
def film_service(settings, redis_client, es_client):
    return FilmService(redis=redis_client, elastic=es_client)


@pytest.fixture(scope="function")
def person_service(settings, redis_client, es_client):
    return PersonService(redis=redis_client, elastic=es_client)


@pytest_asyncio.fixture(scope="function")
async def es_write_data(es_client):
    async def inner(data, index):
        bulk_query = _get_es_bulk_query(data, index, "id")
        str_query = "\n".join(bulk_query) + "\n"
        await es_client.indices.delete(index=index, allow_no_indices=True, ignore_unavailable=True)
        await es_client.indices.create(index=index, mappings=es_mappings[index])

        response = await es_client.bulk(operations=str_query, refresh=True)
        if response["errors"]:
            raise Exception("Ошибка записи данных в Elasticsearch")

    yield inner

    await es_client.options(ignore_status=[400, 404]).delete_by_query(
        index="*", body={"query": {"match_all": {}}}, refresh=True
    )


@pytest_asyncio.fixture(scope="function")
async def redis_write_data(redis_client):
    async def inner(key, data):
        return await redis_client.set(key, data)

    yield inner

    await redis_client.flushall()


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
