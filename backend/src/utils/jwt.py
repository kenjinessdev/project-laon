# utils/jwt.py
from datetime import datetime, timedelta
from jose import jwt
from src.core.config import settings


def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + expires_delta
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_access_token(user_id: str):
    print("=== DEBUG: Access Token Settings ===")
    print(f"JWT_SECRET: {settings.JWT_SECRET}")
    print(f"JWT_ALGORITHM: {settings.JWT_ALGORITHM}")
    print(
        f"ACCESS_TOKEN_EXPIRE_MINUTES: {settings.ACCESS_TOKEN_EXPIRE_MINUTES}")
    return create_token({"sub": user_id}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))


def create_refresh_token(user_id: str):
    return create_token({"sub": user_id}, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))


def decode_token(token: str):
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
