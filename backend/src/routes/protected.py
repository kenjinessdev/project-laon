# routes/protected.py
from fastapi import APIRouter, Depends
from src.dependencies.auth import get_current_user, require_role

role_router = APIRouter()


@role_router.get("/me")
async def me(user=Depends(get_current_user)):
    return user


@role_router.get("/farmer-only")
async def farmer(user=Depends(require_role("farmer"))):
    return {"message": "Welcome Farmer"}


@role_router.get("/customer-only")
async def customer(user=Depends(require_role("customer"))):
    return {"message": "Welcome Customer"}
