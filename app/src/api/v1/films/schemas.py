from uuid import UUID

from pydantic import BaseModel


class DetailedFilm(BaseModel):
    id: UUID
    title: str
    imdb_rating: float
    description: str
    genre: list[str]
    actors: list[str]
    writers: list[str]
    directors: list[str]


class ShortenedFilm(BaseModel):
    id: UUID
    title: str
    imdb_rating: float
