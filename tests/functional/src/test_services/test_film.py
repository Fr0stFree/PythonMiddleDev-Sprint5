from unittest.mock import Mock
from uuid import UUID

import pytest
from elastic_transport import ApiResponseMeta
from elasticsearch import NotFoundError
from faker import Faker

from functional.src.factories import FilmFactory
from models import Film
from services import FilmService

fake = Faker()


@pytest.mark.asyncio
async def test_get_existing_film_from_elastic(film_service: FilmService) -> None:
    looking_film_id = UUID(fake.uuid4())
    film_service.redis.get.return_value = None
    film_service.elastic.get.return_value = {"_source": FilmFactory.create(id=looking_film_id).model_dump()}

    film = await film_service.get_by_id(looking_film_id)

    assert isinstance(film, Film)
    assert film.id == looking_film_id
    film_service.redis.get.assert_awaited_once_with(f"film#{film.id}")
    film_service.elastic.get.assert_awaited_once_with(index=FilmService.elastic_index, id=str(looking_film_id))


@pytest.mark.asyncio
async def test_get_existing_film_from_redis(film_service: FilmService) -> None:
    looking_film_id = UUID(fake.uuid4())
    film_service.redis.get.return_value = FilmFactory.create(id=looking_film_id).model_dump_json()

    film = await film_service.get_by_id(looking_film_id)

    assert isinstance(film, Film)
    assert film.id == looking_film_id
    film_service.redis.get.assert_awaited_once_with(f"film#{film.id}")
    film_service.elastic.get.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_non_existing_film(film_service: FilmService) -> None:
    looking_film_id = UUID(fake.uuid4())
    film_service.redis.get.return_value = None
    film_service.elastic.get.side_effect = NotFoundError(message="", meta=Mock(spec_set=ApiResponseMeta), body={})

    film = await film_service.get_by_id(looking_film_id)

    assert film is None
    film_service.redis.get.assert_awaited_once_with(f"film#{looking_film_id}")
    film_service.elastic.get.assert_awaited_once_with(index=FilmService.elastic_index, id=str(looking_film_id))


@pytest.mark.asyncio
async def test_get_many_films_from_elastic(film_service: FilmService) -> None:
    film_service.redis.exists.return_value = False
    film_service.elastic.search.return_value = {
        "hits": {
            "hits": [
                {"_source": FilmFactory.create().model_dump()},
                {"_source": FilmFactory.create().model_dump()},
            ]
        }
    }

    films = await film_service.get_many(query={}, params={})

    assert len(films) == 2
    assert all(isinstance(film, Film) for film in films)
    film_service.redis.exists.assert_awaited_once()
    film_service.redis.lrange.assert_not_awaited()
    film_service.elastic.search.assert_awaited_once_with(index=FilmService.elastic_index, query={}, params={})


@pytest.mark.asyncio
async def get_many_films_from_redis(film_service: FilmService) -> None:
    film_service.redis.exists.return_value = True
    film_service.redis.lrange.return_value = [
        FilmFactory.create().model_dump_json(),
        FilmFactory.create().model_dump_json(),
    ]

    films = await film_service.get_many(query={}, params={})

    assert len(films) == 2
    assert all(isinstance(film, Film) for film in films)
    film_service.redis.exists.assert_awaited_once()
    film_service.redis.lrange.assert_awaited_once()
    film_service.elastic.search.assert_not_awaited()


@pytest.mark.asyncio
async def get_non_existing_films(film_service: FilmService) -> None:
    film_service.redis.exists.return_value = False
    film_service.elastic.search.return_value = {"hits": {"hits": []}}

    films = await film_service.get_many(query={}, params={})

    assert films == []
    film_service.redis.exists.assert_awaited_once()
    film_service.redis.lrange.assert_not_awaited()
    film_service.elastic.search.assert_awaited_once_with(index=FilmService.elastic_index, query={}, params={})
