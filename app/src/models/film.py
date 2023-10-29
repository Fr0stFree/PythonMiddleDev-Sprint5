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
    director: list[PersonWithoutFilms]

    @classmethod
    def load_model(cls, source):
        genre = [{'id': uuid.uuid4(), 'name': name} for name in source.get('genre', [])]
        director = [{'id': uuid.uuid4(), 'name': name} for name in source.get('director', [])]
        source['genre'] = genre
        source['director'] = director
        return cls(**source)


