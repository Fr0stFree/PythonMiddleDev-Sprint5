from http import HTTPStatus

import pytest
from functional.src.factories import GenreFactory


@pytest.mark.asyncio
async def test_query_genre(es_write_data, make_get_request, settings, genre_service):
    genre = GenreFactory.create()
    await es_write_data([genre.model_dump(mode="json")], index=genre_service.elastic_index)

    response = await make_get_request({"id": str(genre.id)}, endpoint=f"{settings.app_genres_endpoint}/{genre.id}")

    assert response["status"] == HTTPStatus.OK
    assert response["body"] == genre.model_dump(mode="json")


@pytest.mark.asyncio
async def test_query_not_existing_genre(es_write_data, make_get_request, settings, genre_service):
    genre = GenreFactory.create()
    fake_id = "00000000-0000-0000-0000-000000000000"
    await es_write_data([genre.model_dump(mode="json")], index=genre_service.elastic_index)

    response = await make_get_request({"id": fake_id}, endpoint=f"{settings.app_genres_endpoint}/{fake_id}")

    assert response["status"] == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_query_invalid_uuid_genre(make_get_request, settings):
    fake_id = "some-bullshit"

    response = await make_get_request({"id": fake_id}, endpoint=f"{settings.app_genres_endpoint}/{fake_id}")

    assert response["status"] == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_query_many_genres(es_write_data, make_get_request, settings, genre_service):
    genres = [GenreFactory.create() for _ in range(10)]
    await es_write_data([genre.model_dump(mode="json") for genre in genres], index=genre_service.elastic_index)

    response = await make_get_request({}, endpoint=settings.app_genres_endpoint)

    assert response["status"] == HTTPStatus.OK
    assert len(response["body"]) == len(genres)


@pytest.mark.asyncio
async def test_query_specific_genres(es_write_data, make_get_request, settings, genre_service):
    genres = [GenreFactory.create() for _ in range(10)]
    await es_write_data([genre.model_dump(mode="json") for genre in genres], index=genre_service.elastic_index)

    response = await make_get_request({"search": genres[0].name}, endpoint=settings.app_genres_endpoint)

    assert response["status"] == HTTPStatus.OK
    assert len(response["body"]) == 1
    assert response["body"][0] == genres[0].model_dump(exclude={"description"}, mode="json")


@pytest.mark.asyncio
async def test_query_not_existing_genres(es_write_data, make_get_request, settings, genre_service):
    genres = [GenreFactory.create() for _ in range(10)]
    await es_write_data([genre.model_dump(mode="json") for genre in genres], index=genre_service.elastic_index)

    response = await make_get_request({"search": "qweuiasdnasedkjhqwwe"}, endpoint=settings.app_genres_endpoint)

    assert response["status"] == HTTPStatus.OK
    assert len(response["body"]) == 0
