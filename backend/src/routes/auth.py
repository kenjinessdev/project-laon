# routes/auth.py
from fastapi import APIRouter, HTTPException
from src.db.prisma import prisma
from src.utils.security import hash_password, verify_password
from src.utils.jwt import create_access_token, create_refresh_token
from src.models.user import UserCreate, LoginSchema, User
from datetime import datetime
# from src.models.user import UserOut, LoginSchema

auth_router = APIRouter()


@auth_router.post("/register", response_model=User)
async def register(user: UserCreate):
    existing = await prisma.user.find_unique(where={"email": user.email})
    if existing:
        raise HTTPException(400, "Email already registered")
    birthday_datetime = datetime.combine(user.birthday, datetime.min.time())
    new_user = await prisma.user.create(data={
        "first_name": user.first_name,
        "middle_name": user.middle_name,
        "last_name": user.last_name,
        "suffix": user.suffix,
        "profile_image_url": user.profile_image_url,
        "email": user.email,
        "password": hash_password(user.password),
        "phone_number": user.phone_number,
        "gender": user.gender,
        "birthday": birthday_datetime,
        "role": user.role
    })
    return new_user


@auth_router.post("/login")
async def login(creds: LoginSchema):
    user = await prisma.user.find_unique(where={"email": creds.email})
    if not user or not verify_password(creds.password, user.password):
        raise HTTPException(401, "Invalid credentials")
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer"
    }
