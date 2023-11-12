import uuid

import pytest


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"search": "Name"}, {"status": 200, "length": 10}),
        ({"search": "Без имени"}, {"status": 200, "length": 0}),
        ({"page_size": "20"}, {"status": 200, "length": 20}),
    ],
)
@pytest.mark.asyncio
async def test_search_persons(es_write_data, query_data, expected_answer, make_get_request, settings, person_service):
    es_data = [
        {
            "id": str(uuid.uuid4()),
            "name": "Name",
            "films": [
                {
                    "id": "ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95",
                    "roles": ["Action", "Sci-Fi"],
                },
                {
                    "id": "ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95",
                    "roles": ["Action", "Sci-Fi"],
                },
            ],
        }
        for _ in range(50)
    ]

    await es_write_data(es_data, person_service.elastic_index)

    response = await make_get_request(query_data, settings.app_persons_endpoint)

    assert response["status"] == expected_answer["status"]
    assert len(response["body"]) == expected_answer["length"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"id": "ef86b8ff-3c82-4d31-ad8e-72b69f4e3f91"}, {"status": 200}),
        ({"id": "00000000-0000-0000-0000-00000000000"}, {"status": 422}),
        ({"id": "200"}, {"status": 422}),
    ],
)
@pytest.mark.asyncio
async def test_person_item(es_write_data, query_data, expected_answer, make_get_request, settings, person_service):
    es_data = [
        {
            "id": "ef86b8ff-3c82-4d31-ad8e-72b69f4e3f91",
            "name": "Name",
            "films": [
                {
                    "id": "ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95",
                    "roles": ["Action", "Sci-Fi"],
                },
                {
                    "id": "ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95",
                    "roles": ["Action", "Sci-Fi"],
                },
            ],
        }
    ]
    await es_write_data(es_data, person_service.elastic_index)

    response = await make_get_request(query_data, endpoint=f"{settings.app_persons_endpoint}/{query_data['id']}")

    assert response["status"] == expected_answer["status"]
