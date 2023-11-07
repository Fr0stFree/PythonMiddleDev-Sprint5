import pytest
import json
from elasticsearch import AsyncElasticsearch
from .settings import Settings


def get_es_bulk_query(es_data, es_index, es_id_field) -> list:
    bulk_query = []
    for row in es_data:
        bulk_query.extend(
            [json.dumps({"index": {"_index": es_index, "_id": row[es_id_field]}}), json.dumps(row)]
        )
    return bulk_query


@pytest.fixture(scope='session')
async def es_client():
    es_client = AsyncElasticsearch(hosts='http://localhost:9200')
    yield es_client
    await es_client.close()


@pytest.fixture
def es_write_data(es_client):
    async def inner(data):
        bulk_query = get_es_bulk_query(data, 'persons', 'id')
        str_query = '\n'.join(bulk_query) + '\n'
        response = await es_client.bulk(operations=str_query, refresh=True)

        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture
def es_clear_data(es_client):
    async def inner(index):
        await es_client.delete_by_query(index='persons', body={"query": {"match_all": {}}})

    return inner
