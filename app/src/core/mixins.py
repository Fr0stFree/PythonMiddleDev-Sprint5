from typing import Generic, Type, TypeVar

T = TypeVar("T")


class Singleton(Generic[T]):
    _instance = None

    def __new__(cls: Type[T], *args, **kwargs) -> T:
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> T:
        if cls._instance is None:
            raise RuntimeError(f"{cls} is not initialized.")
        return cls._instance
