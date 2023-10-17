import uvicorn
from fastapi import FastAPI

from config.settings import Settings
from movies.router import movies_router


if __name__ == '__main__':
    settings = Settings()
    app = FastAPI(title=settings.project_name, debug=settings.debug)
    app.include_router(movies_router)

    uvicorn.run('main:app', host=settings.server_host, port=settings.server_port, reload=True)