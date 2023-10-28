from typing import Optional
from uuid import UUID

import orjson
from elasticsearch import NotFoundError

from core.constants import FILM_CACHE_EXPIRE, MOVIES_INDEX_NAME
from models.film import Film
from .mixins import ServiceMixin


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
            doc = await self.elastic.get(index=MOVIES_INDEX_NAME, id=film_id)
        except NotFoundError:
            return None
        return Film(**doc["_source"])

    async def _film_from_cache(self, film_id: UUID) -> Optional[Film]:
        data = await self.redis.get(str(film_id))
        if not data:
            return None
        return Film.model_validate(orjson.loads(data))

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(str(film.id), film.model_dump_json(), FILM_CACHE_EXPIRE)

    async def get_many(self, sort_params=None, search_params=None) -> list[Film]:
        docs = await self.elastic.search(
            index=MOVIES_INDEX_NAME,
            query={"match": {"title": {"query": search_params}}},
            sort=sort_params
        )
        return [Film(**doc["_source"]) for doc in docs["hits"]["hits"]]
