from typing import Optional
from uuid import UUID

from models.person import Person
from .mixins import ServiceMixin


class PersonService(ServiceMixin):
    async def get_by_id(self, person_id: UUID) -> Optional[Person]:
        pass

    async def get_many(self, **kwargs) -> list[Person]:
        pass
