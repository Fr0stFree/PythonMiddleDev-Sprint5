from unittest.mock import Mock
from uuid import UUID

from elastic_transport import ApiResponseMeta
from elasticsearch import NotFoundError
from faker import Faker

from films.constants import MOVIES_INDEX_NAME
from films.models import Film
from films.services import FilmService

from ..factories import FilmFactory

fake = Faker()


class TestFilmService:
	async def test_get_existing_film_from_elastic(self, film_service: FilmService) -> None:
		looking_film_id = UUID(fake.uuid4())
		film_service.redis.get.return_value = None
		film_service.elastic.get.return_value = {"_source": FilmFactory.create(uuid=looking_film_id).model_dump()}

		film = await film_service.get_by_id(looking_film_id)

		assert isinstance(film, Film)
		assert film.uuid == looking_film_id
		film_service.redis.get.assert_awaited_once_with(str(looking_film_id))
		film_service.elastic.get.assert_awaited_once_with(index=MOVIES_INDEX_NAME, uuid=looking_film_id)
		film_service.redis.set.assert_awaited_once()

	async def test_get_existing_film_from_redis(self, film_service: FilmService) -> None:
		looking_film_id = UUID(fake.uuid4())
		film_service.redis.get.return_value = FilmFactory.create(uuid=looking_film_id).model_dump()

		film = await film_service.get_by_id(looking_film_id)

		assert isinstance(film, Film)
		assert film.uuid == looking_film_id
		film_service.redis.get.assert_awaited_once_with(str(looking_film_id))
		film_service.elastic.get.assert_not_awaited()
		film_service.redis.set.assert_not_awaited()

	async def test_get_non_existing_film(self, film_service: FilmService) -> None:
		looking_film_id = UUID(fake.uuid4())
		film_service.redis.get.return_value = None
		film_service.elastic.get.side_effect = NotFoundError(message="", meta=Mock(spec_set=ApiResponseMeta), body={})

		film = await film_service.get_by_id(looking_film_id)

		assert film is None
		film_service.redis.get.assert_awaited_once_with(str(looking_film_id))
		film_service.elastic.get.assert_awaited_once_with(index=MOVIES_INDEX_NAME, uuid=looking_film_id)
		film_service.redis.set.assert_not_awaited()


class TestGenreService:
	pass


class TestPersonService:
	pass
