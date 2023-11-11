import json

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch

from functional.settings import Settings


@pytest.fixture(scope="session")
def settings():
    return Settings()


@pytest.fixture
def es_write_data(settings):
    es_client = AsyncElasticsearch(hosts=f"http://{settings.elastic_host}:{settings.elastic_port}")

    async def inner(data, index):
        bulk_query = _get_es_bulk_query(data, index, "id")
        str_query = "\n".join(bulk_query) + "\n"
        try:
            response = await es_client.bulk(operations=str_query, refresh=True)
            if response["errors"]:
                raise Exception("Ошибка записи данных в Elasticsearch")
        finally:
            await es_client.close()

    return inner


@pytest.fixture(scope="function", autouse=True)
async def es_clear_data(settings):
    es_client = AsyncElasticsearch(hosts=f"http://{settings.elastic_host}:{settings.elastic_port}")
    yield
    await es_client.delete_by_query(index="*", body={"query": {"match_all": {}}})
    await es_client.close()


@pytest.fixture
def make_get_request(settings):
    async def inner(endpoint, query_data):
        url = f"http://{settings.app_host}:{settings.app_port}/api/v1/{endpoint}"
        session = aiohttp.ClientSession()

        async with session.get(url, params=query_data) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
        await session.close()
        return {"body": body, "status": status, "headers": headers}

    return inner


@pytest.fixture
def make_get_request_id(settings):
    async def inner(endpoint, query_data):
        url = f'http://{settings.app_host}:{settings.app_port}/api/v1/{endpoint}/{query_data["id"]}'
        session = aiohttp.ClientSession()

        async with session.get(url) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
        await session.close()
        return {"body": body, "status": status, "headers": headers}

    return inner


def _get_es_bulk_query(es_data, es_index, es_id_field) -> list:
    bulk_query = []
    for row in es_data:
        bulk_query.extend([json.dumps({"index": {"_index": es_index, "_id": row[es_id_field]}}), json.dumps(row)])
    return bulk_query
