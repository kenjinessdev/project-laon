# from pydantic import BaseSettings
from pydantic_settings import BaseSettings


class Settings(BaseSettings):  # type: ignore
    DATABASE_URL: str
    JWT_SECRET: str
    SESSION_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Add these for Google
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # Add these for Facebook
    FACEBOOK_CLIENT_ID: str
    FACEBOOK_CLIENT_SECRET: str
    FACEBOOK_REDIRECT_URI: str

    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str

    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
