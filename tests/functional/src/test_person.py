import datetime
import uuid
import json

import aiohttp
import pytest

from elasticsearch import AsyncElasticsearch
from tests.functional.utils.settings import Settings

@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'search': 'Name'},
                {'status': 200, 'length': 10}
        ),
        (
                {'search': 'Без имени'},
                {'status': 200, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(es_write_data, query_data, expected_answer, make_get_request, es_clear_data):
    settings = Settings()
    es_data = [{
        'id': str(uuid.uuid4()),
        'name': 'Name',
        'films': [
            {'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'roles': ['Action', 'Sci-Fi']},
            {'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'roles': ['Action', 'Sci-Fi']}
        ]
    } for _ in range(10)]

    await es_write_data(es_data)

    response = await make_get_request(settings.app_persons_endpoint, query_data)
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']

    await es_clear_data(settings.es_index_persons)

