from uuid import UUID

from core.mixins import CustomBaseModel


class Genre(CustomBaseModel):
    id: UUID
    name: str
