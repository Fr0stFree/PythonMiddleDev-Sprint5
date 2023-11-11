from http import HTTPStatus

import pytest

from functional.src.factories import GenreFactory


@pytest.mark.asyncio
async def test_query_genre(es_write_data, make_get_request_id, settings):
    genre = GenreFactory.create()
    genre.id = str(genre.id)
    await es_write_data([genre.model_dump()], index=settings.es_index_genres)

    response = await make_get_request_id(settings.app_genres_endpoint, {"id": genre.id})

    assert response["status"] == HTTPStatus.OK
    assert response["body"] == genre.model_dump()


@pytest.mark.asyncio
async def test_query_not_existing_genre(es_write_data, make_get_request_id, settings):
    genre = GenreFactory.create()
    genre.id = str(genre.id)
    await es_write_data([genre.model_dump()], index=settings.es_index_genres)

    response = await make_get_request_id(settings.app_genres_endpoint, {"id": "00000000-0000-0000-0000-000000000000"})

    assert response["status"] == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_query_invalid_uuid_genre(make_get_request_id, settings):
    response = await make_get_request_id(settings.app_genres_endpoint, {"id": "some-bullshit"})

    assert response["status"] == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_query_many_genres(es_write_data, make_get_request, settings):
    genres = [GenreFactory.create() for _ in range(10)]
    [setattr(genre, "id", str(genre.id)) for genre in genres]
    await es_write_data([genre.model_dump() for genre in genres], index=settings.es_index_genres)

    response = await make_get_request(settings.app_genres_endpoint, {})

    assert response["status"] == HTTPStatus.OK
    assert len(response["body"]) == len(genres)


@pytest.mark.asyncio
async def test_query_specific_genres(es_write_data, make_get_request, settings):
    genres = [GenreFactory.create() for _ in range(10)]
    [setattr(genre, "id", str(genre.id)) for genre in genres]
    await es_write_data([genre.model_dump() for genre in genres], index=settings.es_index_genres)

    response = await make_get_request(settings.app_genres_endpoint, {"search": genres[0].name})

    assert response["status"] == HTTPStatus.OK
    assert len(response["body"]) == 1
    assert response["body"][0] == genres[0].model_dump(exclude={"description"})


@pytest.mark.asyncio
async def test_query_not_existing_genres(es_write_data, make_get_request, settings):
    genres = [GenreFactory.create() for _ in range(10)]
    [setattr(genre, "id", str(genre.id)) for genre in genres]
    await es_write_data([genre.model_dump() for genre in genres], index=settings.es_index_genres)

    response = await make_get_request(settings.app_genres_endpoint, {"search": "some-bullshit"})

    assert response["status"] == HTTPStatus.OK
    assert len(response["body"]) == 0
