from uuid import UUID

from pydantic import BaseModel


class ShortenedGenre(BaseModel):
    id: UUID
    name: str


class DetailedGenre(BaseModel):
    id: UUID
    name: str
    description: str
