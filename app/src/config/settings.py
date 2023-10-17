from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    project_name: str = Field("Cinema-0.1", env="PROJECT_NAME")
    debug: bool = Field(..., env="DEBUG")
    secret_key: str = Field(..., env="SECRET_KEY")
