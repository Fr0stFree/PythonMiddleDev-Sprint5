from uuid import UUID

from .base import CustomBaseModel


class Genre(CustomBaseModel):
    id: UUID
    name: str
