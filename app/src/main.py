import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from api.router import router
from core.config import Settings
from db import BaseApp, ElasticApp, RedisApp

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # create connections to the databases
    redis: BaseApp = RedisApp(host=settings.redis_host, port=settings.redis_port)
    elastic = ElasticApp(host=settings.elastic_host, port=settings.elastic_port)
    await asyncio.gather(redis.connect(), elastic.connect())
    # yield control back to the main program
    yield
    # after the main program is finished, close all connections
    await asyncio.gather(redis.disconnect(), elastic.disconnect())


app = FastAPI(
    title=settings.project_name,
    debug=settings.debug,
    openapi_url=settings.openapi_documentation_url,
    docs_url=settings.api_documentation_url,
    lifespan=lifespan,
)
app.include_router(router, prefix="/api")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="main:app",
        host=settings.app_host,
        port=settings.app_port,
        log_config=settings.log_config,
        log_level=logging.DEBUG if settings.debug else logging.INFO,
        reload=settings.debug,
    )
