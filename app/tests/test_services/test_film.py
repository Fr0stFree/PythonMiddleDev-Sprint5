from unittest.mock import Mock
from uuid import UUID

import pytest
from elastic_transport import ApiResponseMeta
from elasticsearch import NotFoundError
from faker import Faker

from models import Film
from services import FilmService

from ..factories import FilmFactory

fake = Faker()


@pytest.mark.skip("Will be fixed in the next lesson, hopefully")
async def test_get_existing_film_from_elastic(film_service: FilmService) -> None:
    looking_film_id = UUID(fake.uuid4())
    film_service.redis.get.return_value = None
    film_service.elastic.get.return_value = {"_source": FilmFactory.create(id=looking_film_id).model_dump()}

    film = await film_service.get_by_id(looking_film_id)

    assert isinstance(film, Film)
    assert film.id == looking_film_id
    film_service.redis.get.assert_awaited_once_with(f"film#{film.id}")
    film_service.elastic.get.assert_awaited_once_with(index=FilmService.elastic_index, id=looking_film_id)
    film_service.redis.set.assert_awaited_once_with(
        f"film#{film.id}", film.model_dump_json(), FilmService.cache_expires.total_seconds()
    )


@pytest.mark.skip("Will be fixed in the next lesson, hopefully")
async def test_get_existing_film_from_redis(film_service: FilmService) -> None:
    looking_film_id = UUID(fake.uuid4())
    film_service.redis.get.return_value = FilmFactory.create(id=looking_film_id).model_dump()

    film = await film_service.get_by_id(looking_film_id)

    assert isinstance(film, Film)
    assert film.id == looking_film_id
    film_service.redis.get.assert_awaited_once_with(f"film#{film.id}")
    film_service.elastic.get.assert_not_awaited()
    film_service.redis.set.assert_not_awaited()


@pytest.mark.skip("Will be fixed in the next lesson, hopefully")
async def test_get_non_existing_film(film_service: FilmService) -> None:
    looking_film_id = UUID(fake.uuid4())
    film_service.redis.get.return_value = None
    film_service.elastic.get.side_effect = NotFoundError(message="", meta=Mock(spec_set=ApiResponseMeta), body={})

    film = await film_service.get_by_id(looking_film_id)

    assert film is None
    film_service.redis.get.assert_awaited_once_with(f"film#{looking_film_id}")
    film_service.elastic.get.assert_awaited_once_with(index=FilmService.elastic_index, id=looking_film_id)
    film_service.redis.set.assert_not_awaited()
