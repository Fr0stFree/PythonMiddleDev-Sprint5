from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from services import GenreService

from api.v1.dependencies import get_pagination_params
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
    search: str = Query(None, max_length=50),
    genre_service: GenreService = Depends(GenreService.get_instance),
    pagination_params: dict = Depends(get_pagination_params)
) -> list[ShortenedGenre]:
    query = {"match_all": {}} if search is None else {"multi_match": {"query": search, "fields": ["name"]}}
    params = pagination_params
    genres = await genre_service.get_many(query, params)
    return genres
