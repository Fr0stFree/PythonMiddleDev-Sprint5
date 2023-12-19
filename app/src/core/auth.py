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
        print(credentials)
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

# {
#     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXZAZGV2LmNvbSIsImlhdCI6MTcwMzAyMzM0NSwibmJmIjoxNzAzMDIzMzQ1LCJqdGkiOiIzNjkzMjVjOS1lYWIxLTQyYTgtYWFhNS1jOTQzNTAxY2RiMzQiLCJleHAiOjE3MDMyODI1NDUsInR5cGUiOiJhY2Nlc3MiLCJmcmVzaCI6ZmFsc2V9.Tu8Io4UpmuTyhynS7mjMH_2yfZyFs6dWhsSZhxV-HP4",
#     "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXZAZGV2LmNvbSIsImlhdCI6MTcwMzAyMzM0NSwibmJmIjoxNzAzMDIzMzQ1LCJqdGkiOiIyMmU3OGNjNy1hYTI2LTQ2YWUtYWRlZC0xN2FhZmUwZWQ3MzIiLCJleHAiOjE3MDMwMjQ1NDUsInR5cGUiOiJyZWZyZXNoIiwiYWNjZXNzX2p0aSI6IjM2OTMyNWM5LWVhYjEtNDJhOC1hYWE1LWM5NDM1MDFjZGIzNCJ9.Qi5ddtFyNcCZ3mq9ehQycpRAXtGbIXn34kQa38Hn8vU",
#     "token_type": "bearer"
# }