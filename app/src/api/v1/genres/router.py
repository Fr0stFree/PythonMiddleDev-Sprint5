from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from services import GenreService

from api.v1.dependencies import get_pagination_params, get_search_query_by_name
from .schemas import DetailedGenre, ShortenedGenre

router = APIRouter()


@router.get(
    "/{genre_id}",
    description="Returns information about a specific genre by ID",
)
async def genre_details(
    genre_id: UUID = Path(...), genre_service: GenreService = Depends(GenreService.get_instance)
) -> DetailedGenre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")

    return genre


@router.get(
    "/",
    description="Returns a list genres",
)
async def genre_list(
    search: dict = Depends(get_search_query_by_name),
    genre_service: GenreService = Depends(GenreService.get_instance),
    pagination_params: dict = Depends(get_pagination_params),
) -> list[ShortenedGenre]:
    genres = await genre_service.get_many(search, pagination_params)
    return genres
