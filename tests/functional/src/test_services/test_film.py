import pytest

from models import Film
from services import FilmService
from tests.functional.src.factories import FilmFactory


@pytest.mark.asyncio
async def test_get_existing_film_from_elastic(es_write_data, film_service: FilmService) -> None:
    film = FilmFactory.create()
    await es_write_data([film.model_dump(mode="json")], index=film_service.elastic_index)

    result = await film_service.get_by_id(film.id)

    assert isinstance(result, Film)
    assert result == film
    film_service.cache_app.get_one.assert_called_once_with(film.id, film_service.model_class_name)
    film_service.search_engine.get_one.assert_called_once_with(str(film.id), film_service.elastic_index)


@pytest.mark.asyncio
async def test_get_existing_film_from_redis(redis_write_data, film_service: FilmService) -> None:
    film = FilmFactory.create()
    await redis_write_data(f"film#{film.id}", film.model_dump_json())

    result = await film_service.get_by_id(film.id)

    assert isinstance(result, Film)
    assert result == film
    film_service.cache_app.get_one.assert_called_once_with(film.id, film_service.model_class_name)
    film_service.search_engine.get_one.assert_not_called()


@pytest.mark.asyncio
async def test_get_non_existing_film(redis_write_data, film_service: FilmService) -> None:
    film = FilmFactory.create()

    result = await film_service.get_by_id(film.id)

    assert result is None
    film_service.cache_app.get_one.assert_called_once_with(film.id, film_service.model_class_name)
    film_service.search_engine.get_one.assert_called_once_with(str(film.id), film_service.elastic_index)
