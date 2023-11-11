from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from services import FilmService

from .schemas import DetailedFilm, ShortenedFilm

router = APIRouter()


@router.get(
    "/{film_id}",
    description="Returns information about a specific film by ID",
)
async def film_details(
    film_id: UUID = Path(...), film_service: FilmService = Depends(FilmService.get_instance)
) -> DetailedFilm:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not found")
    return DetailedFilm(
        **film.dict(exclude={"actors", "writers", "directors"}),
        actors=[actor.name for actor in film.actors],
        writers=[writer.name for writer in film.writers],
        directors=[director.name for director in film.directors],
    )


@router.get(
    "/",
    description="Returns a list films",
)
async def film_list(
    search: Annotated[str | None, Query(max_length=50)] = None,
    sort: Annotated[Literal["imdb_rating:asc", "imdb_rating:desc"], Query()] = "imdb_rating:asc",
    film_service: FilmService = Depends(FilmService.get_instance),
    page_number: int = Query(None, ge=0),
    page_size: int = Query(None, ge=1),
) -> list[ShortenedFilm]:
    params = {"sort": sort, "size": page_size, "from": page_number}
    query = {"match_all": {}} if search is None else {"multi_match": {"query": search}}
    films = await film_service.get_many(query, params)
    return films
