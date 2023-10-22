from uuid import UUID

from pydantic import Field

from core.mixins import CustomBaseModel


class Genre(CustomBaseModel):
    uuid: UUID
    name: str


class _InnerPersonRoles(CustomBaseModel):
    uuid: UUID  # film uuid
    roles: list[str]


class Person(CustomBaseModel):
    uuid: UUID
    full_name: str
    films: list[_InnerPersonRoles]


class _InnerPerson(Person):
    films: list[UUID] = Field(exclude=True)


class Film(CustomBaseModel):
    uuid: UUID
    title: str
    imdb_rating: float
    description: str
    genre: list[Genre]
    actors: list[_InnerPerson]
    writers: list[_InnerPerson]
    directors: list[_InnerPerson]
