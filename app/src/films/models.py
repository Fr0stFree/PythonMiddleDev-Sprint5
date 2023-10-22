from uuid import UUID

from core.mixins import CustomBaseModel


class Genre(CustomBaseModel):
    uuid: UUID
    name: str


class PersonRoles(CustomBaseModel):
    uuid: UUID  # film uuid
    roles: list[str]


class Person(CustomBaseModel):
    uuid: UUID
    full_name: str
    films: list[PersonRoles]


class PersonWithoutFilms(CustomBaseModel):
    uuid: UUID
    full_name: str


class Film(CustomBaseModel):
    uuid: UUID
    title: str
    imdb_rating: float
    description: str
    genre: list[Genre]
    actors: list[PersonWithoutFilms]
    writers: list[PersonWithoutFilms]
    directors: list[PersonWithoutFilms]
