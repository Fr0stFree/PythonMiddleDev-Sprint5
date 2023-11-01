from uuid import UUID

from pydantic import BaseModel


class _PersonRoles(BaseModel):
    id: UUID
    roles: list[str]


class DetailedPerson(BaseModel):
    id: UUID
    name: str
    films: list[_PersonRoles]
