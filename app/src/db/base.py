from abc import ABC, abstractmethod

from core.mixins import Singleton


class BaseApp(ABC, Singleton):
    def __init__(self, host: str, port: int, **kwargs) -> None:
        self._host = host
        self._port = port

    @abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self) -> None:
        raise NotImplementedError
