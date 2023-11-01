from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from services import GenreService

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
    page_number: int = Query(None, ge=0),
    page_size: int = Query(None, ge=1),
) -> list[ShortenedGenre]:
    query = {"match_all": {}} if search is None else {"multi_match": {"query": search, "fields": ["name"]}}
    params = {"size": page_size, "from": page_number}
    genres = await genre_service.get_many(query, params)
    return genres
