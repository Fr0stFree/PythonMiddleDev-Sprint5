from core.mixins import CustomBaseModel


class Film(CustomBaseModel):
    id: str
    title: str
    description: str
