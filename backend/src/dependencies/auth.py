# dependencies/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.utils.jwt import decode_token
from src.db.prisma import prisma

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    user_id = payload.get("sub")
    user = await prisma.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(401, "User not found")
    return user


def require_role(role: str):
    async def checker(user=Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(403, "Insufficient permissions")
        return user
    return checker
