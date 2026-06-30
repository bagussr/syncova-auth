from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings


class BaseSettings(BaseSettings):
    DB_URL: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    JWT_SECRET: str
    ENV: str

    class Config:
        env_file = ".env"


def get_settings() -> BaseSettings:
    return BaseSettings()


Settings = Annotated[BaseSettings, Depends(get_settings)]
