import datetime as dt
from typing import ClassVar

from pydantic import BaseModel

from models import Genre

from .base import BaseService


class GenreService(BaseService):
    model_class: ClassVar[BaseModel] = Genre
    elastic_index: ClassVar[str] = "movies"
    cache_expires: ClassVar[dt.timedelta] = dt.timedelta(minutes=5)
