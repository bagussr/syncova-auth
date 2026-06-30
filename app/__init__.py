from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_URL: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    JWT_SECRET: str


settings = Settings()
