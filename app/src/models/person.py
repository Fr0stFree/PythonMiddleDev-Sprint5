from uuid import UUID
from pydantic import Field
from core.mixins import CustomBaseModel


class PersonRoles(CustomBaseModel):
    id: UUID  # film uuid
    roles: list[str]


class Person(CustomBaseModel):
    uuid: UUID = Field(alias='id')
    full_name: str = Field(alias='name')
    films: list[PersonRoles]

    @classmethod
    def load_model(cls, source):
        roles = [{'id': uuid.uuid4()} for name in source.get('roles', [])]
        source['films'] = roles
        return cls(**source)


class PersonWithoutFilms(CustomBaseModel):
    id: UUID
    name: str
