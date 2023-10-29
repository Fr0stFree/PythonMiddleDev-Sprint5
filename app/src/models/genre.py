from uuid import UUID
from pydantic import Field
from core.mixins import CustomBaseModel


class Genre(CustomBaseModel):
    uuid: UUID = Field(alias='id')
    name: str

    @classmethod
    def load_model(cls, source):
        return cls(**source)


class DetailGenre(Genre):
    description: str

    @classmethod
    def load_model(cls, source):
        return cls(**source)

