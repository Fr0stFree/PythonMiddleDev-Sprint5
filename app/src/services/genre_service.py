from typing import Optional
from uuid import UUID

from models.genre import Genre, DetailGenre
from .mixins import ServiceMixin

from core.constants import GENRES_INDEX_NAME


class GenreService(ServiceMixin):
    async def get_by_id(self, genre_id: UUID) -> Optional[DetailGenre]:
        doc = await self.elastic.get(
            index=GENRES_INDEX_NAME,
            id=genre_id,
        )
        return DetailGenre.load_model(doc["_source"])

    async def get_many(self, **kwargs) -> list[Genre]:
        docs = await self.elastic.search(
            index=GENRES_INDEX_NAME,
            # query={"multi_match": {"query": search_params}},
            # params={"size": page_size, "from": page_number}
            # sort=sort_params
        )
        return [Genre.load_model(doc["_source"]) for doc in docs["hits"]["hits"]]
