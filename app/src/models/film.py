import uuid

from core.mixins import CustomBaseModel
from .genre import Genre
from .person import PersonWithoutFilms


class Film(CustomBaseModel):
    id: uuid.UUID
    title: str
    imdb_rating: float
    description: str
    genre: list[str]
    actors: list[PersonWithoutFilms]
    writers: list[PersonWithoutFilms]
    directors: list[PersonWithoutFilms]
