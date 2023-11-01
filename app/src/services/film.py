import datetime as dt
from typing import ClassVar, Type
from uuid import UUID

from pydantic import BaseModel

from models import Film

from .base import BaseService


class FilmService(BaseService):
    model_class: ClassVar[Type[BaseModel]] = Film
    elastic_index: ClassVar[str] = "movies"
    cache_expires: ClassVar[dt.timedelta] = dt.timedelta(minutes=5)

    async def get_films_by_person(self, person_id: UUID, params: dict) -> list[Film]:
        query = {
            "bool": {
                "should": [
                    {"nested": {"path": "actors", "query": {"bool": {"must": [{"match": {"actors.id": person_id}}]}}}},
                    {
                        "nested": {
                            "path": "writers",
                            "query": {"bool": {"must": [{"match": {"writers.id": person_id}}]}},
                        }
                    },
                    {
                        "nested": {
                            "path": "directors",
                            "query": {"bool": {"must": [{"match": {"directors.id": person_id}}]}},
                        }
                    },
                ]
            }
        }
        return await self.get_many(query, params)
