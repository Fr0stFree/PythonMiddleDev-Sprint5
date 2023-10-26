from typing import Self
from uuid import UUID

from pydantic import BaseModel

from models.person import Person


class _PersonRoles(BaseModel):
    uuid: UUID
    roles: list[str]


class DetailedPerson(BaseModel):
    uuid: UUID
    full_name: str
    films: list[_PersonRoles]

    @classmethod
    def from_elastic_schema(cls, person: Person) -> Self:
        return cls(**person.model_dump())
