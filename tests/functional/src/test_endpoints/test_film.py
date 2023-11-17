from http import HTTPStatus

import pytest

from api.v1.films.schemas import DetailedFilm, ShortenedFilm
from tests.functional.src.factories import FilmFactory

pytestmark = pytest.mark.asyncio


async def test_query_film(es_write_data, make_get_request, settings, film_service):
    film = FilmFactory.create()
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


async def test_query_not_existing_film(es_write_data, make_get_request, settings, film_service):
    film = FilmFactory.create()
    fake_id = "00000000-0000-0000-0000-000000000000"
    await es_write_data([film.model_dump(mode="json")], index=film_service.elastic_index)

    response = await make_get_request({"id": fake_id}, endpoint=f"{settings.app_films_endpoint}/{fake_id}")

    assert response["status"] == HTTPStatus.NOT_FOUND


async def test_query_invalid_uuid_film(make_get_request, settings):
    fake_id = "foobar"

    response = await make_get_request({"id": fake_id}, endpoint=f"{settings.app_films_endpoint}/{fake_id}")

    assert response["status"] == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_query_many_films(es_write_data, make_get_request, settings, film_service):
    films = [FilmFactory.create() for _ in range(10)]
    await es_write_data([film.model_dump(mode="json") for film in films], index=film_service.elastic_index)

    response = await make_get_request({}, endpoint=settings.app_films_endpoint)

    assert response["status"] == HTTPStatus.OK
    assert len(response["body"]) == len(films)


async def test_query_specific_films(es_write_data, make_get_request, settings, film_service):
    films = [FilmFactory.create() for _ in range(10)]
    shortened_film = ShortenedFilm(**films[0].model_dump(mode="json"))
    print(shortened_film.model_dump(mode="json"))

    await es_write_data([film.model_dump(mode="json") for film in films], index=film_service.elastic_index)

    response = await make_get_request({"search": shortened_film.title}, endpoint=settings.app_films_endpoint)

    assert response["status"] == HTTPStatus.OK
    assert len(response["body"]) < 10
    assert shortened_film.model_dump(mode="json") in response["body"]


async def test_query_not_existing_films(es_write_data, make_get_request, settings, film_service):
    films = [FilmFactory.create() for _ in range(10)]
    await es_write_data([film.model_dump(mode="json") for film in films], index=film_service.elastic_index)

    response = await make_get_request({"search": "foobar123123asdzxc"}, endpoint=settings.app_genres_endpoint)

    assert response["status"] == HTTPStatus.OK
    assert len(response["body"]) == 0
