# dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.utils.jwt import decode_token
from src.db.prisma import prisma
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     payload = decode_token(token)
#     user_id = payload.get("sub")
#     user = await prisma.user.find_unique(where={"id": user_id})
#     if not user:
#         raise HTTPException(401, "User not found")
#     return user
#
#


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = await prisma.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


def require_role(role: str):
    async def checker(user=Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(403, "Insufficient permissions")
        return user
    return checker
