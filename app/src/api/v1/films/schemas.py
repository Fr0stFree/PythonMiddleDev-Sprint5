from typing import Self
from uuid import UUID

from pydantic import BaseModel

from models.film import Film


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
            uuid=film.id,
            actors=[actor.name for actor in film.actors],
            writers=[writer.name for writer in film.writers],
            directors=[director.name for director in film.directors],
            **film.model_dump(exclude={"actors", "writers", "directors"}),
        )


class ShortenedFilm(BaseModel):
    uuid: UUID
    title: str
    imdb_rating: float

    @classmethod
    def from_elastic_schema(cls, film: Film) -> Self:
        return cls(
            uuid=film.id,
            **film.model_dump(exclude={"description", "genre", "actors", "writers", "directors"})
        )
