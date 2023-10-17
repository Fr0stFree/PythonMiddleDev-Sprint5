from typing import Type, TypeVar, Generic

import orjson
from pydantic import BaseModel

T = TypeVar("T")


class Singleton(Generic[T]):
    _instance = None

    def __new__(class_: Type[T], *args, **kwargs) -> T:
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_)
        return class_._instance

    @classmethod
    def get_instance(cls) -> T:
        if cls._instance is None:
            raise RuntimeError(f"{cls} is not initialized")
        return cls._instance


class CustomBaseModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = lambda v, *, default: orjson.dumps(v, default=default).decode()

