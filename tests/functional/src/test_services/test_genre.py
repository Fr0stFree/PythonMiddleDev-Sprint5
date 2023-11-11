from unittest.mock import Mock
from uuid import UUID

import pytest
from elastic_transport import ApiResponseMeta
from elasticsearch import NotFoundError
from faker import Faker

from functional.src.factories import GenreFactory
from models import Genre
from services import GenreService

fake = Faker()


@pytest.mark.asyncio
async def test_get_existing_genre_from_elastic(genre_service: GenreService) -> None:
    looking_genre_id = UUID(fake.uuid4())
    genre_service.redis.get.return_value = None
    genre_service.elastic.get.return_value = {"_source": GenreFactory.create(id=looking_genre_id).model_dump()}

    genre = await genre_service.get_by_id(looking_genre_id)

    assert isinstance(genre, Genre)
    assert genre.id == looking_genre_id
    genre_service.redis.get.assert_awaited_once_with(f"genre#{genre.id}")
    genre_service.elastic.get.assert_awaited_once_with(index=GenreService.elastic_index, id=str(looking_genre_id))


@pytest.mark.asyncio
async def test_get_existing_genre_from_redis(genre_service: GenreService) -> None:
    looking_genre_id = UUID(fake.uuid4())
    genre_service.redis.get.return_value = GenreFactory.create(id=looking_genre_id).model_dump_json()

    genre = await genre_service.get_by_id(looking_genre_id)

    assert isinstance(genre, Genre)
    assert genre.id == looking_genre_id
    genre_service.redis.get.assert_awaited_once_with(f"genre#{genre.id}")
    genre_service.elastic.get.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_non_existing_genre(genre_service: GenreService) -> None:
    looking_genre_id = UUID(fake.uuid4())
    genre_service.redis.get.return_value = None
    genre_service.elastic.get.side_effect = NotFoundError(message="", meta=Mock(spec_set=ApiResponseMeta), body={})

    genre = await genre_service.get_by_id(looking_genre_id)

    assert genre is None
    genre_service.redis.get.assert_awaited_once_with(f"genre#{looking_genre_id}")
    genre_service.elastic.get.assert_awaited_once_with(index=GenreService.elastic_index, id=str(looking_genre_id))


@pytest.mark.asyncio
async def test_get_many_genres_from_elastic(genre_service: GenreService) -> None:
    genre_service.redis.exists.return_value = False
    genre_service.elastic.search.return_value = {
        "hits": {
            "hits": [
                {"_source": GenreFactory.create().model_dump()},
                {"_source": GenreFactory.create().model_dump()},
            ]
        }
    }

    genres = await genre_service.get_many(query={}, params={})

    assert len(genres) == 2
    assert all(isinstance(genre, Genre) for genre in genres)
    genre_service.redis.exists.assert_awaited_once()
    genre_service.redis.lrange.assert_not_awaited()
    genre_service.elastic.search.assert_awaited_once_with(index=GenreService.elastic_index, query={}, params={})


@pytest.mark.asyncio
async def get_many_genres_from_redis(genre_service: GenreService) -> None:
    genre_service.redis.exists.return_value = True
    genre_service.redis.lrange.return_value = [
        GenreFactory.create().model_dump_json(),
        GenreFactory.create().model_dump_json(),
    ]

    genres = await genre_service.get_many(query={}, params={})

    assert len(genres) == 2
    assert all(isinstance(genre, Genre) for genre in genres)
    genre_service.redis.exists.assert_awaited_once()
    genre_service.redis.lrange.assert_awaited_once()
    genre_service.elastic.search.assert_not_awaited()


@pytest.mark.asyncio
async def get_non_existing_genres(genre_service: GenreService) -> None:
    genre_service.redis.exists.return_value = False
    genre_service.elastic.search.return_value = {"hits": {"hits": []}}

    genres = await genre_service.get_many(query={}, params={})

    assert genres == []
    genre_service.redis.exists.assert_awaited_once()
    genre_service.redis.lrange.assert_not_awaited()
    genre_service.elastic.search.assert_awaited_once_with(index=GenreService.elastic_index, query={}, params={})
