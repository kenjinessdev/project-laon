from pydantic import BaseSettings


class Settings(BaseSettings):  # type: ignore
    DATABASE_URL: str
    JWT_SECRET: str
    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
