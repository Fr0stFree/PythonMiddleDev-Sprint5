import pytest
from functional.src.factories import GenreFactory

from models import Genre
from services import GenreService


@pytest.mark.asyncio
async def test_get_existing_genre_from_elastic(es_write_data, genre_service: GenreService) -> None:
    genre = GenreFactory.create()
    await es_write_data([genre.model_dump(mode="json")], index=genre_service.elastic_index)

    result = await genre_service.get_by_id(genre.id)

    assert isinstance(result, Genre)
    assert result == genre
    genre_service.redis.get.assert_called_once_with(f"genre#{genre.id}")
    genre_service.elastic.get.assert_called_once_with(index=genre_service.elastic_index, id=str(genre.id))


@pytest.mark.asyncio
async def test_get_existing_genre_from_redis(redis_write_data, genre_service: GenreService) -> None:
    genre = GenreFactory.create()
    await redis_write_data(f"genre#{genre.id}", genre.model_dump_json())

    result = await genre_service.get_by_id(genre.id)

    assert isinstance(result, Genre)
    assert result == genre
    genre_service.redis.get.assert_called_once_with(f"genre#{genre.id}")
    genre_service.elastic.get.assert_not_called()


@pytest.mark.asyncio
async def test_get_non_existing_genre(redis_write_data, genre_service: GenreService) -> None:
    genre = GenreFactory.create()

    result = await genre_service.get_by_id(genre.id)

    assert result is None
    genre_service.redis.get.assert_called_once_with(f"genre#{genre.id}")
    genre_service.elastic.get.assert_called_once_with(index=genre_service.elastic_index, id=str(genre.id))
