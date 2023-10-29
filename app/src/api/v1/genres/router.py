from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from services import GenreService

from .schemas import DetailedGenre, ShortenedGenre

router = APIRouter()


@router.get("/{genre_id}")
async def genre_details(
    genre_id: UUID = Path(...), genre_service: GenreService = Depends(GenreService.get_instance)
) -> DetailedGenre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found")

    return genre


@router.get("/")
async def genre_list(
    search: str = Query(None, max_length=50), genre_service: GenreService = Depends(GenreService.get_instance)
) -> list[ShortenedGenre]:
    query = {"match_all": {}} if search is None else {"multi_match": {"query": search, "fields": ["name"]}}
    params = {"size": 10}
    genres = await genre_service.get_many(query, params)
    return genres
