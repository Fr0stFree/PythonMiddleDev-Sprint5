import http
import time
from typing import Optional

from jose import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.config import Settings

settings = Settings()


def decode_token(token: str) -> Optional[dict]:
    try:
        decoded_token = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return decoded_token if decoded_token['exp'] >= time.time() else None
    except Exception:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail='Invalid authorization code.')
        if not credentials.scheme == 'Bearer':
            raise HTTPException(status_code=http.HTTPStatus.UNAUTHORIZED, detail='Only Bearer token might be accepted')
        decoded_token = self.parse_token(credentials.credentials)
        if not decoded_token:
            raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail='Invalid or expired token.')
        return decoded_token

    @staticmethod
    def parse_token(jwt_token: str) -> Optional[dict]:
        return decode_token(jwt_token)


security_jwt = JWTBearer()
