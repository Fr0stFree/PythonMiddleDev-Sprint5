from uuid import UUID

from .base import CustomBaseModel


class NestedFilm(CustomBaseModel):
    id: UUID
    title: str
    imdb_rating: float


class NestedPerson(CustomBaseModel):
    id: UUID
    name: str


class Film(CustomBaseModel):
    id: UUID
    title: str
    imdb_rating: float
    description: str
    genre: list[str]
    actors: list[NestedPerson]
    writers: list[NestedPerson]
    directors: list[NestedPerson]
