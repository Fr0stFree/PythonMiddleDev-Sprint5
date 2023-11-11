import pytest
import aiohttp
import json
from elasticsearch import AsyncElasticsearch

from dotenv import find_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings
from functional.settings import Settings


def get_es_bulk_query(es_data, es_index, es_id_field) -> list:
    bulk_query = []
    for row in es_data:
        bulk_query.extend(
            [json.dumps({"index": {"_index": es_index, "_id": row[es_id_field]}}), json.dumps(row)]
        )
    return bulk_query


@pytest.fixture
def es_write_data():
    async def inner(data):
        settings = Settings()
        bulk_query = get_es_bulk_query(data, settings.es_index_persons, 'id')
        str_query = '\n'.join(bulk_query) + '\n'

        es_client = AsyncElasticsearch(hosts=f'http://{settings.elastic_host}:{settings.elastic_port}')
        response = await es_client.bulk(operations=str_query, refresh=True)
        await es_client.close()
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture
def es_clear_data():
    async def inner(index):
        settings = Settings()
        es_client = AsyncElasticsearch(hosts=f'http://{settings.elastic_host}:{settings.elastic_port}')
        await es_client.delete_by_query(index=index, body={"query": {"match_all": {}}})
        await es_client.close()

    return inner


@pytest.fixture
def make_get_request():
    async def inner(endpoint, query_data):
        settings = Settings()
        url = f'http://{settings.app_host}:{settings.app_port}/api/v1/{endpoint}'
        session = aiohttp.ClientSession()

        async with session.get(url, params=query_data) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
        await session.close()
        return {'body': body, 'status': status, 'headers': headers}
    return inner


@pytest.fixture
def make_get_request_id():
    async def inner(endpoint, query_data):
        settings = Settings()
        url = f'http://{settings.app_host}:{settings.app_port}/api/v1/{endpoint}/{query_data["id"]}'
        session = aiohttp.ClientSession()

        async with session.get(url) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
        await session.close()
        return {'body': body, 'status': status, 'headers': headers}

    return inner
