from typing import Self
from uuid import UUID

from pydantic import BaseModel

from films.models import Film, Genre, Person


class DetailedFilm(BaseModel):
    uuid: UUID
    title: str
    imdb_rating: float
    description: str
    genre: list[str]
    actors: list[str]
    writers: list[str]
    directors: list[str]

    @classmethod
    def from_elastic_schema(cls, film: Film) -> Self:
        return cls(
            genre=[genre.name for genre in film.genre],
            actors=[actor.full_name for actor in film.actors],
            writers=[writer.full_name for writer in film.writers],
            directors=[director.full_name for director in film.directors],
            **film.model_dump(exclude={"genre", "actors", "writers", "directors"}),
        )


class ShortenedFilm(BaseModel):
    uuid: UUID
    title: str
    imdb_rating: float

    @classmethod
    def from_elastic_schema(cls, film: Film) -> Self:
        return cls(**film.model_dump(exclude={"description", "genre", "actors", "writers", "directors"}))


class DetailedGenre(BaseModel):
    uuid: UUID
    name: str

    @classmethod
    def from_elastic_schema(cls, genre: Genre) -> Self:
        return cls(**genre.model_dump())


class _PersonRoles(BaseModel):
    uuid: UUID
    roles: list[str]


class DetailedPerson(BaseModel):
    uuid: UUID
    full_name: str
    films: list[_PersonRoles]

    @classmethod
    def from_elastic_schema(cls, person: Person) -> Self:
        return cls(**person.model_dump())
