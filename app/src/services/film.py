import datetime as dt
from typing import ClassVar

from pydantic import BaseModel

from models import Film

from .base import BaseService


class FilmService(BaseService):
    model_class: ClassVar[BaseModel] = Film
    elastic_index: ClassVar[str] = "movies"
    cache_expires: ClassVar[dt.timedelta] = dt.timedelta(minutes=5)
