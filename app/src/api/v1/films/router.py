from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from services import FilmService
from .schemas import DetailedFilm, ShortenedFilm

SORTING_PARAMS = ['imdb_rating:asc', 'imdb_rating:desc']

router = APIRouter(prefix="/films", tags=['Films'])


def sorting_params(sort: str = Query(None)):
    if sort not in SORTING_PARAMS:
        return None
    return sort


@router.get("/{film_id}")
async def film_details(
    film_id: UUID = Path(...), film_service: FilmService = Depends(FilmService.get_instance)
) -> DetailedFilm:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not found")
    return DetailedFilm.from_elastic_schema(film)


@router.get("/")
async def film_list(
    search: Annotated[str | None, Query(max_length=50)] = None,
    sort: Annotated[str | None, Depends(sorting_params)] = None,
    film_service: FilmService = Depends(FilmService.get_instance),
) -> list[ShortenedFilm]:
    films = await film_service.get_many(sort_params=sort, search_params=search)
    return [ShortenedFilm.from_elastic_schema(film) for film in films]
