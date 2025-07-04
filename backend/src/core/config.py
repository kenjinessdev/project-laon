# from pydantic import BaseSettings
from pydantic_settings import BaseSettings


class Settings(BaseSettings):  # type: ignore
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
