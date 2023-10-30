from uuid import UUID

from .base import CustomBaseModel
from .person import NestedPerson


class NestedFilm(CustomBaseModel):
    id: UUID
    title: str
    imdb_rating: float


class Film(CustomBaseModel):
    id: UUID
    title: str
    imdb_rating: float
    description: str
    genre: list[str]
    actors: list[NestedPerson]
    writers: list[NestedPerson]
    directors: list[NestedPerson]
