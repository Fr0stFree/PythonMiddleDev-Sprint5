from uuid import UUID

from core.mixins import CustomBaseModel


class PersonRoles(CustomBaseModel):
    id: UUID  # film uuid
    roles: list[str]


class Person(CustomBaseModel):
    id: UUID
    name: str
    films: list[PersonRoles]


class PersonWithoutFilms(CustomBaseModel):
    id: UUID
    name: str
