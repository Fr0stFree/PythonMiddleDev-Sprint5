from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from services import PersonService

from ..films.schemas import ShortenedFilm
from .schemas import DetailedPerson

router = APIRouter()


@router.get("/{person_id}")
async def person_details(
    person_id: UUID = Path(...), person_service: PersonService = Depends(PersonService.get_instance)
) -> DetailedPerson:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")

    return person


@router.get("/")
async def person_list(
    query: str,
    page_number: int = Query(None),
    page_size: int = Query(None),
    person_service: PersonService = Depends(PersonService.get_instance),
) -> list[DetailedPerson]:
    params = {"size": page_size, "from": page_number}
    query = {"multi_match": {"query": query}}
    persons = await person_service.get_many(query, params)
    return persons


@router.get("/{person_id}/films")
async def person_films(
    person_id: UUID = Path(...),
    person_service: PersonService = Depends(PersonService.get_instance),
) -> list[ShortenedFilm]:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")

    films = await person_service.get_films_by_person(person_id)
    return films
