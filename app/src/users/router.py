from http import HTTPStatus

from fastapi import APIRouter, Depends


router = APIRouter(prefix="/users", tags=["users"])