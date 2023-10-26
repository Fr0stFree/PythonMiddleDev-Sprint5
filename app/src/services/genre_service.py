from typing import Optional
from uuid import UUID

from models.genre import Genre
from .mixins import ServiceMixin


class GenreService(ServiceMixin):
    async def get_by_id(self, genre_id: UUID) -> Optional[Genre]:
        pass

    async def get_many(self, **kwargs) -> list[Genre]:
        pass
