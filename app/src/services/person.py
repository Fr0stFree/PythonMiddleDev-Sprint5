import datetime as dt
from typing import ClassVar, Type
from uuid import UUID

from pydantic import BaseModel

from models import NestedFilm, Person

from .base import BaseService


class PersonService(BaseService):
    model_class: ClassVar[Type[BaseModel]] = Person
    elastic_index: ClassVar[str] = "persons"
    cache_expires: ClassVar[dt.timedelta] = dt.timedelta(minutes=5)

    async def get_films_by_person(self, person_id: UUID) -> list[NestedFilm]:
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
        return await super().get_many(query, params={"size": 100})
