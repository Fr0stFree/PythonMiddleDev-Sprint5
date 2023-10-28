import datetime as dt
from typing import ClassVar, Type

from pydantic import BaseModel

from models import Person

from .base import BaseService


class PersonService(BaseService):
    model_class: ClassVar[Type[BaseModel]] = Person
    elastic_index: ClassVar[str] = "movies"
    cache_expires: ClassVar[dt.timedelta] = dt.timedelta(minutes=5)
