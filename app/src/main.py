import asyncio
import logging

import uvicorn
from fastapi import FastAPI

from api.v1.films.router import router as films_router
from api.v1.genres.router import router as genres_router
from api.v1.persons.router import router as persons_router
from core.config import Settings
from db import ElasticApp, RedisApp

settings = Settings()
app = FastAPI(
    title=settings.project_name,
    debug=settings.debug,
    openapi_url=settings.openapi_documentation_url,
    docs_url=settings.api_documentation_url,
)

app.include_router(films_router, prefix="/api/v1")
app.include_router(genres_router, prefix="/api/v1")
app.include_router(persons_router, prefix="/api/v1")

redis = RedisApp(host=settings.redis_host, port=settings.redis_port)
elastic = ElasticApp(host=settings.elastic_host, port=settings.elastic_port)


@app.on_event("startup")
async def startup():
    await asyncio.gather(
        redis.connect(),
        elastic.connect(),
    )


@app.on_event("shutdown")
async def shutdown():
    await asyncio.gather(
        redis.disconnect(),
        elastic.disconnect(),
    )


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.app_host,
        port=settings.app_port,
        log_config=settings.log_config,
        log_level=logging.DEBUG if settings.debug else logging.INFO,
        reload=settings.debug,
    )
