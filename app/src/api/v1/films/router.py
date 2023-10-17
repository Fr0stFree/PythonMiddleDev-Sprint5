from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from films.services import FilmService
from .models import Film

router = APIRouter(prefix="/films")


@router.get("/{film_id}")
async def film_details(film_id: str, film_service: FilmService = Depends(FilmService.get_instance)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")

    return Film(id=film.id, title=film.title)
