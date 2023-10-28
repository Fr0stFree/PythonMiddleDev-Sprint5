from fastapi.routing import APIRouter

from .films.router import router as films_router
from .genres.router import router as genres_router
from .persons.router import router as persons_router

router = APIRouter()

router.include_router(persons_router, prefix="/persons", tags=["Persons"])
router.include_router(genres_router, prefix="/genres", tags=["Genres"])
router.include_router(films_router, prefix="/films", tags=["Films"])
