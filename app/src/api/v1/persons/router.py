from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from services import FilmService, PersonService
from api.v1.films.schemas import ShortenedFilm
from .schemas import DetailedPerson

router = APIRouter(prefix="/persons", tags=["Persons"])


@router.get("/")
async def person_list(
        search: str = Query(None),
        sort: str = Query(None),
        person_service: PersonService = Depends(PersonService.get_instance),
) -> list[DetailedPerson]:
    persons = await person_service.get_many(sort_params=sort, search_params=search)
    return [DetailedPerson.from_elastic_schema(person) for person in persons]


@router.get("/{person_id}")
async def person_details(
        person_id: UUID = Path(...), person_service: PersonService = Depends(PersonService.get_instance)
) -> DetailedPerson:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")

    return DetailedPerson.from_elastic_schema(person)


@router.get("/persons/{person_id}/films")
async def person_films(
        person_id: UUID = Path(...),
        person_service: PersonService = Depends(PersonService.get_instance),
        film_service: FilmService = Depends(FilmService.get_instance),
) -> list[ShortenedFilm]:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")

    films = await film_service.get_many(
        search_params=f"actors:{person_id} OR writers:{person_id} OR directors:{person_id}"
    )
    return [ShortenedFilm.from_elastic_schema(film) for film in films]
