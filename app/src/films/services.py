from typing import Optional, Self
from uuid import UUID

from elasticsearch import NotFoundError

from .constants import FILM_CACHE_EXPIRE, MOVIES_INDEX_NAME
from .mixins import ServiceMixin
from .models import Film, Genre, Person


class FilmService(ServiceMixin):
    async def get_by_id(self, film_id: UUID) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)
        return film

    async def _get_film_from_elastic(self, film_id: UUID) -> Optional[Film]:
        try:
            doc = await self.elastic.get(index=MOVIES_INDEX_NAME, uuid=film_id)
        except NotFoundError:
            return None
        return Film(**doc["_source"])

    async def _film_from_cache(self, film_id: UUID) -> Optional[Film]:
        data = await self.redis.get(str(film_id))
        if not data:
            return None
        return Film.model_validate(data)

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(str(film.uuid), film.model_dump_json(), FILM_CACHE_EXPIRE)

    async def get_many(self, sort_params=None, search_params=None) -> list[Film]:
        pass


class GenreService(ServiceMixin):
    async def get_by_id(self, genre_id: UUID) -> Optional[Genre]:
        pass

    async def get_many(self, **kwargs) -> list[Genre]:
        pass


class PersonService(ServiceMixin):
    async def get_by_id(self, person_id: UUID) -> Optional[Person]:
        pass

    async def get_many(self, **kwargs) -> list[Person]:
        pass
