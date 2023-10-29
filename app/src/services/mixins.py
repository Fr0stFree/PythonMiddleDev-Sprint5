from typing_extensions import Self

from core.mixins import Singleton
from db import ElasticApp, RedisApp


class ServiceMixin(Singleton):
    def __init__(self):
        self.redis = RedisApp.redis_client()
        self.elastic = ElasticApp.elastic_client()

    @classmethod
    def get_instance(cls) -> Self:
        """Create an instance automatically if not exist."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
