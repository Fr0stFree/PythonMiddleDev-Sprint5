import uuid

from core.mixins import CustomBaseModel
from .genre import Genre
from .person import PersonWithoutFilms


class Film(CustomBaseModel):
    id: uuid.UUID
    title: str
    imdb_rating: float
    description: str
    genre: list[Genre]
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


