from typing_extensions import Self
from uuid import UUID

from pydantic import BaseModel

from models.genre import Genre


class Genre(BaseModel):
    uuid: UUID
    name: str

    @classmethod
    def from_elastic_schema(cls, genre: Genre) -> Self:
        return cls(**genre.model_dump())


class DetailedGenre(BaseModel):
    uuid: UUID
    name: str
    description: str

    @classmethod
    def from_elastic_schema(cls, genre: Genre) -> Self:
        return cls(**genre.model_dump())
