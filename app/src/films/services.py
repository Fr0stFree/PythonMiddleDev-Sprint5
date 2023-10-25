from typing import ClassVar
import datetime as dt

from pydantic import BaseModel

from .base_service import BaseService
from .constants import FILM_CACHE_EXPIRES, GENRE_CACHE_EXPIRES, MOVIES_INDEX_NAME, PERSON_CACHE_EXPIRES
from .models import Film, Genre, Person


class FilmService(BaseService):
    elastic_index: ClassVar[str] = MOVIES_INDEX_NAME
    cache_expires: ClassVar[dt.timedelta] = FILM_CACHE_EXPIRES
    model_class: ClassVar[BaseModel] = Film


class GenreService(BaseService):
    elastic_index: ClassVar[str] = MOVIES_INDEX_NAME
    cache_expires: ClassVar[dt.timedelta] = GENRE_CACHE_EXPIRES
    model_class: ClassVar[BaseModel] = Genre


class PersonService(BaseService):
    elastic_index: ClassVar[str] = MOVIES_INDEX_NAME
    cache_expires: ClassVar[dt.timedelta] = PERSON_CACHE_EXPIRES
    model_class: ClassVar[BaseModel] = Person
