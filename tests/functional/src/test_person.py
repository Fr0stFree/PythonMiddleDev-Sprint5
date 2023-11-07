import datetime
import uuid
import json

import aiohttp
import pytest

from elasticsearch import AsyncElasticsearch



@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'search': 'Name'},
                {'status': 200, 'length': 10}
        ),
        (
                {'search': 'Mashed potato'},
                {'status': 200, 'length': 0}
        ),
        (
                {'search': 'Mashed potato'},
                {'status': 200, 'length': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(es_write_data, es_clear_data, query_data, expected_answer):

    es_data = [{
        'id': str(uuid.uuid4()),
        'name': 'Name',
        'films': [
            {'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'roles': ['Action', 'Sci-Fi']},
            {'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'roles': ['Action', 'Sci-Fi']}
        ]
    } for _ in range(60)]

    await es_write_data(es_data)



    # 3. Запрашиваем данные из ES по API

    session = aiohttp.ClientSession()
    url = 'http://localhost:8000/api/v1/persons/'
    async with session.get(url, params=query_data) as response:
        body = await response.json()
        headers = response.headers
        status = response.status
    await session.close()

    # 4. Проверяем ответ
    # assert 200 == 100
    assert status == expected_answer['status']
    assert len(body) == expected_answer['length']
    await es_clear_data(es_data)
