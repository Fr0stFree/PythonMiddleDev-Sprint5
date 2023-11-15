import pytest

from models import Film

pytestmark = pytest.mark.asyncio


async def test_get_existing_film_from_elastic(es_write_data, film_service, film):
    await es_write_data([film.model_dump(mode="json")], index=film_service.elastic_index)

    result = await film_service.get_by_id(film.id)

    assert isinstance(result, Film)
    assert result == film
    film_service.redis.get.assert_called_once_with(f"film#{film.id}")
    film_service.elastic.get.assert_called_once_with(index=film_service.elastic_index, id=str(film.id))


async def test_get_existing_film_from_redis(redis_write_data, film_service, film):
    await redis_write_data(f"film#{film.id}", film.model_dump_json())

    result = await film_service.get_by_id(film.id)

    assert isinstance(result, Film)
    assert result == film
    film_service.redis.get.assert_called_once_with(f"film#{film.id}")
    film_service.elastic.get.assert_not_called()


async def test_get_non_existing_film(film_service, film):
    result = await film_service.get_by_id(film.id)

    assert result is None
    film_service.redis.get.assert_called_once_with(f"film#{film.id}")
    film_service.elastic.get.assert_called_once_with(index=film_service.elastic_index, id=str(film.id))
