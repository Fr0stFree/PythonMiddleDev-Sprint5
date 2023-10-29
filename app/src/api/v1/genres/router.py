from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from services import GenreService
from .schemas import DetailedGenre, Genre

router = APIRouter(prefix="/genres", tags=['Genres'])


@router.get("/genres")
async def genre_list(genre_service: GenreService = Depends(GenreService.get_instance)) -> list[Genre]:
    genres = await genre_service.get_many()
    return [Genre.from_elastic_schema(genre) for genre in genres]


@router.get("/genres/{genre_id}")
async def genre_details(
        genre_id: UUID = Path(...), genre_service: GenreService = Depends(GenreService.get_instance)
) -> DetailedGenre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")

    return DetailedGenre.from_elastic_schema(genre)
