import pytest

from models import Genre

pytestmark = pytest.mark.asyncio


async def test_get_existing_genre_from_elastic(es_write_data, genre_service, genre):
    await es_write_data([genre.model_dump(mode="json")], index=genre_service.elastic_index)

    result = await genre_service.get_by_id(genre.id)

    assert isinstance(result, Genre)
    assert result == genre
    genre_service.cache_app.get_one.assert_called_once_with(genre.id, genre_service.model_class_name)
    genre_service.search_engine.get_one.assert_called_once_with(str(genre.id), genre_service.elastic_index)


async def test_get_existing_genre_from_redis(redis_write_data, genre_service, genre):
    await redis_write_data(f"genre#{genre.id}", genre.model_dump_json())

    result = await genre_service.get_by_id(genre.id)

    assert isinstance(result, Genre)
    assert result == genre
    genre_service.cache_app.get_one.assert_called_once_with(genre.id, genre_service.model_class_name)
    genre_service.search_engine.get_one.assert_not_called()


async def test_get_non_existing_genre(genre_service, genre):
    result = await genre_service.get_by_id(genre.id)

    assert result is None
    genre_service.cache_app.get_one.assert_called_once_with(genre.id, genre_service.model_class_name)
    genre_service.search_engine.get_one.assert_called_once_with(str(genre.id), genre_service.elastic_index)
