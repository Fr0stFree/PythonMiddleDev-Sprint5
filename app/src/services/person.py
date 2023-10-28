import datetime as dt
from typing import ClassVar

from pydantic import BaseModel

from models import Person

from .base import BaseService


class PersonService(BaseService):
    model_class: ClassVar[BaseModel] = Person
    elastic_index: ClassVar[str] = "movies"
    cache_expires: ClassVar[dt.timedelta] = dt.timedelta(minutes=5)
