
# routes/auth.py
from fastapi import Request, Response, HTTPException, APIRouter
from src.db.prisma import prisma
from src.utils.security import hash_password, verify_password
from src.utils.jwt import create_access_token, create_refresh_token
from src.models.user import UserCreate, LoginSchema
from datetime import datetime
from src.core.config import settings
from prisma.errors import UniqueViolationError
from src.core.limiter import limiter
from jose import JWTError
from src.utils.jwt import decode_token, issue_tokens
from src.routes.v1.auth.facebook_auth import facebook_router
from src.routes.v1.auth.google_auth import google_router


# from src.models.user import UserOut, LoginSchema

auth_router = APIRouter()

auth_router.include_router(facebook_router)
auth_router.include_router(google_router)


@auth_router.post("/register")
@limiter.limit("5/minute")
async def register(request: Request,  response: Response, user: UserCreate):
    try:
        birthday_datetime = datetime.combine(
            user.birthday, datetime.min.time())
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

        access_token = issue_tokens(new_user.id, response)

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except UniqueViolationError as e:
        message = str(e).lower()

        print("⚠️ UniqueViolationError:", message)

        if "email" in message:
            detail = "Email already registered"
        elif "phone_number" in message:
            detail = "Phone number already registered"
        else:
            detail = "A unique field is already in use"

        raise HTTPException(status_code=400, detail=detail)


@auth_router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, response: Response, creds: LoginSchema):
    user = await prisma.user.find_unique(where={"email": creds.email})
    if not user or not verify_password(creds.password, user.password):
        raise HTTPException(401, "Invalid credentials")

    access_token = issue_tokens(user.id, response)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@auth_router.post("/refresh")
async def refresh_token(request: Request):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(401, "No refresh token found")

    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Invalid token payload")
    except JWTError:
        raise HTTPException(401, "Invalid or expired token")

    return {
        "access_token": create_access_token(user_id),
        "token_type": "bearer"
    }
