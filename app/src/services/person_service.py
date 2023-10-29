from typing import Optional
from uuid import UUID

from models.person import Person
from models.film import FilmBase
from .mixins import ServiceMixin

from core.constants import PERSONS_INDEX_NAME, MOVIES_INDEX_NAME


class PersonService(ServiceMixin):
    async def get_by_id(self, person_id: UUID) -> Optional[Person]:
        doc = await self.elastic.get(
            index=PERSONS_INDEX_NAME,
            id=person_id,
        )
        return Person.load_model(doc["_source"])

    async def get_films_by_person(self, person_id: UUID) -> list[Person]:
        docs = await self.elastic.search(
            index=MOVIES_INDEX_NAME,
            query={"bool": {"should": [
                {"nested": {"path": "actors", "query": {"bool": {"must": [{"match": {"actors.id": person_id}}]}}}},
                {"nested": {"path": "writers", "query": {"bool": {"must": [{"match": {"writers.id": person_id}}]}}}},
                {"nested": {"path": "directors", "query": {"bool": {"must": [{"match": {"directors.id": person_id}}]}}}}
            ]}},
        )
        return [FilmBase.load_model(doc["_source"]) for doc in docs["hits"]["hits"]]

    async def get_many(self, search_params=str, page_number=None, page_size=None) -> list[Person]:
        docs = await self.elastic.search(
            index=PERSONS_INDEX_NAME,
            query={"multi_match": {"query": search_params}},
            params={"size": page_size, "from": page_number}
        )
        return [Person.load_model(doc["_source"]) for doc in docs["hits"]["hits"]]
