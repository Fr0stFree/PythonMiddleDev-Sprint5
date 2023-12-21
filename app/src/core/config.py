from logging import config as logging_config
from pathlib import Path

from dotenv import find_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

from core.logger import LOGGING


class Settings(BaseSettings):
    project_name: str = Field("movies", env="PROJECT_NAME")
    base_dir: Path = Path(__file__).parent.parent
    debug: bool = Field(..., env="DEBUG")
    secret_key: str = Field(..., env="SECRET_KEY")
    app_host: str = Field(..., env="APP_HOST")
    app_port: int = Field(..., env="APP_PORT")

    api_documentation_url: str = "/api/docs"
    openapi_documentation_url: str = "/api/openapi.json"

    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(..., env="REDIS_PORT")

    elastic_host: str = Field(..., env="ELASTIC_HOST")
    elastic_port: int = Field(..., env="ELASTIC_PORT")

    jwt_secret_key: str = Field(default="SOMETHING_REALLY_SECRET", env="SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="ENCRYPTION_ALGORITHM")

    logging_config.dictConfig(LOGGING)

    class Config:
        env_file = find_dotenv(".env")
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def log_config(self) -> dict:
        return LOGGING
