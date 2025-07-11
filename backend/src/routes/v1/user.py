# in routes/user.py or similar
from fastapi import APIRouter, Depends
from src.dependencies.auth import get_current_user
from prisma.models import User

user_router = APIRouter()


@user_router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
