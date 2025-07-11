# utils/jwt.py
from jose import jwt, JWTError
from datetime import datetime, timedelta
from src.core.config import settings


def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + expires_delta
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_access_token(user_id: str):
    print(
        f"ACCESS_TOKEN_EXPIRE_MINUTES: {settings.ACCESS_TOKEN_EXPIRE_MINUTES}")
    return create_token({"sub": user_id}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))


def create_refresh_token(user_id: str):
    return create_token({"sub": user_id}, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))

# def decode_token(token: str):
#     return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])


def decode_token(token: str):
    if not token or len(token.split(".")) != 3:
        raise JWTError("Invalid token format")

    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as e:
        raise JWTError(f"Token decoding failed: {str(e)}")
