from dotenv import find_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = Field("movies", env="PROJECT_NAME")
    debug: bool = Field(..., env="DEBUG")
    secret_key: str = Field(..., env="SECRET_KEY")
    app_host: str = Field(..., env="APP_HOST")
    app_port: int = Field(..., env="APP_PORT")

    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(..., env="REDIS_PORT")

    elastic_host: str = Field(..., env="ELASTIC_HOST")
    elastic_port: int = Field(..., env="ELASTIC_PORT")

    es_index_persons: str = Field("persons")

    class Config:
        env_file = find_dotenv(".env")
        env_file_encoding = "utf-8"
        case_sensitive = False
