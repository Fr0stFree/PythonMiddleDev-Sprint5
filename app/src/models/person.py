from uuid import UUID

from .base import CustomBaseModel


class _PersonRoles(CustomBaseModel):
    id: UUID  # film uuid
    roles: list[str]


class Person(CustomBaseModel):
    id: UUID
    name: str
    films: list[_PersonRoles]
