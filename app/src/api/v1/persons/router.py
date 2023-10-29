from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from services import FilmService, PersonService
from api.v1.films.schemas import ShortenedFilm
from .schemas import DetailedPerson

router = APIRouter(prefix="/persons", tags=["Persons"])


@router.get("/{person_id}")
async def person_details(
        person_id: UUID = Path(...), person_service: PersonService = Depends(PersonService.get_instance)
) -> DetailedPerson:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")

    return DetailedPerson.from_elastic_schema(person)


@router.get("/persons/search/")
async def person_search(
        query: str,
        page_number: int = Query(None),
        page_size: int = Query(None),
        person_service: PersonService = Depends(PersonService.get_instance),
        film_service: FilmService = Depends(FilmService.get_instance),
) -> list[DetailedPerson]:
    persons = await person_service.get_many(page_number=page_number, search_params=query, page_size=page_size)
    return persons


@router.get("/persons/{person_id}/films")
async def person_films(
        person_id: UUID = Path(...),
        person_service: PersonService = Depends(PersonService.get_instance),
        film_service: FilmService = Depends(FilmService.get_instance),
) -> list[ShortenedFilm]:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")

    films = await person_service.get_films_by_person(person_id)
    return films
