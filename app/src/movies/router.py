from http import HTTPStatus

from fastapi import APIRouter, Depends


movies_router = APIRouter(prefix="/movies", tags=["movies"])
