from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from core.mixins import Singleton
from db import RedisApp, ElasticApp
from films.constants import FILM_CACHE_EXPIRE_IN_SECONDS
from films.models import Film


class FilmService(Singleton):
    def __init__(
        self,
        redis: Redis = Depends(RedisApp.get_instance),
        elastic: AsyncElasticsearch = Depends(ElasticApp.get_instance),
    ) -> None:
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)
        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get(index="movies", id=film_id)
        except NotFoundError:
            return None
        return Film(**doc["_source"])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None
        return Film.model_validate(data)

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(film.id, film.model_dump_json(), FILM_CACHE_EXPIRE_IN_SECONDS)
