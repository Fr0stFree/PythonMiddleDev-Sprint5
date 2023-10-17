from pydantic import BaseModel


class Film(BaseModel):
    id: str
    title: str
