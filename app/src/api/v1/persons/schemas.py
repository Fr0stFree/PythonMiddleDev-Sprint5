from uuid import UUID

from pydantic import BaseModel


class _PersonRoles(BaseModel):
    uuid: UUID
    roles: list[str]


class DetailedPerson(BaseModel):
    uuid: UUID
    full_name: str
    films: list[_PersonRoles]
