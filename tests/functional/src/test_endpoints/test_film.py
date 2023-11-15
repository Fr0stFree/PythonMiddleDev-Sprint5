from http import HTTPStatus

import pytest

from api.v1.films.schemas import DetailedFilm, ShortenedFilm


@pytest.mark.asyncio
async def test_query_film(es_write_data, make_get_request, settings, film_service, film):
    detailed_film = DetailedFilm(
        **film.model_dump(exclude={"actors", "writers", "directors"}, mode="json"),
        actors=[actor.name for actor in film.actors],
        writers=[writer.name for writer in film.writers],
        directors=[director.name for director in film.directors],
    )
    await es_write_data([film.model_dump(mode="json")], index=film_service.elastic_index)

    response = await make_get_request({"id": str(film.id)}, endpoint=f"{settings.app_films_endpoint}/{film.id}")

    assert response["status"] == HTTPStatus.OK
    assert response["body"] == detailed_film.model_dump(mode="json")


@pytest.mark.asyncio
async def test_query_not_existing_film(es_write_data, make_get_request, settings, film_service, film):
    fake_id = "00000000-0000-0000-0000-000000000000"
    await es_write_data([film.model_dump(mode="json")], index=film_service.elastic_index)

    response = await make_get_request({"id": fake_id}, endpoint=f"{settings.app_films_endpoint}/{fake_id}")

    assert response["status"] == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_query_invalid_uuid_film(make_get_request, settings):
    fake_id = "foobar"

    response = await make_get_request({"id": fake_id}, endpoint=f"{settings.app_films_endpoint}/{fake_id}")

    assert response["status"] == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_query_many_films(es_write_data, make_get_request, settings, film_service, films):
    await es_write_data([film.model_dump(mode="json") for film in films], index=film_service.elastic_index)

    response = await make_get_request({}, endpoint=settings.app_films_endpoint)

    assert response["status"] == HTTPStatus.OK
    assert len(response["body"]) == len(films)


@pytest.mark.asyncio
async def test_query_specific_films(es_write_data, make_get_request, settings, film_service, films):
    shortened_film = ShortenedFilm(**films[0].model_dump(mode="json"))
    await es_write_data([film.model_dump(mode="json") for film in films], index=film_service.elastic_index)

    response = await make_get_request({"search": shortened_film.title}, endpoint=settings.app_films_endpoint)

    assert response["status"] == HTTPStatus.OK
    assert len(response["body"]) < 10
    assert shortened_film.model_dump(mode="json") in response["body"]


@pytest.mark.asyncio
async def test_query_not_existing_films(es_write_data, make_get_request, settings, film_service, films):
    await es_write_data([film.model_dump(mode="json") for film in films], index=film_service.elastic_index)

    response = await make_get_request({"search": "foobar123123asdzxc"}, endpoint=settings.app_genres_endpoint)

    assert response["status"] == HTTPStatus.OK
    assert len(response["body"]) == 0
