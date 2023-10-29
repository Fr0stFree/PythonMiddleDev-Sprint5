import uuid
from uuid import UUID
from core.mixins import CustomBaseModel
from .genre import Genre
from .person import PersonWithoutFilms

from pydantic import Field


class FilmBase(CustomBaseModel):
    uuid: UUID = Field(alias='id')
    title: str
    imdb_rating: float

    @classmethod
    def load_model(cls, source):
        return cls(**source)


class Film(CustomBaseModel):
    id: UUID
    title: str
    imdb_rating: float
    description: str
    genre: list[str]
    actors: list[PersonWithoutFilms]
    writers: list[PersonWithoutFilms]
    directors: list[PersonWithoutFilms]
