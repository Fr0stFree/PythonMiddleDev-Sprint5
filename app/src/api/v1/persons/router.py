from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from services import FilmService, PersonService

from ..films.schemas import ShortenedFilm
from .schemas import DetailedPerson

router = APIRouter()


@router.get(
    "/{person_id}",
    description="Returns information about a specific person by ID",
)
async def person_details(
    person_id: UUID = Path(...), person_service: PersonService = Depends(PersonService.get_instance)
) -> DetailedPerson:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")

    return person


@router.get(
    "/",
    description="Returns a list persons",
)
async def person_list(
    search: str = Query(None, max_length=50),
    page_number: int = Query(None, ge=0),
    page_size: int = Query(None, ge=1),
    person_service: PersonService = Depends(PersonService.get_instance),
) -> list[DetailedPerson]:
    params = {"size": page_size, "from": page_number}
    query = {"match_all": {}} if search is None else {"multi_match": {"query": search, "fields": ["name"]}}
    persons = await person_service.get_many(query, params)
    return persons


@router.get(
    "/{person_id}/films",
    summary="Films by person ID",
    description="Returns a list of films for a specific person by ID",
)
async def person_films(
    person_id: UUID = Path(...),
    person_service: PersonService = Depends(PersonService.get_instance),
    film_service: FilmService = Depends(FilmService.get_instance),
    page_number: int = Query(None, ge=0),
    page_size: int = Query(None, ge=1),
) -> list[ShortenedFilm]:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    params = {"size": page_size, "from": page_number}
    films = await film_service.get_films_by_person(person_id, params)
    return films
