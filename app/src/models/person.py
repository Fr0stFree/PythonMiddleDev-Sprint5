from uuid import UUID

from .base import CustomBaseModel


class NestedPersonRoles(CustomBaseModel):
    id: UUID  # film uuid
    roles: list[str]


class NestedPerson(CustomBaseModel):
    id: UUID
    name: str


class Person(CustomBaseModel):
    id: UUID
    name: str
    films: list[NestedPersonRoles]
