# routes/auth.py
from fastapi import APIRouter, HTTPException
from src.db.prisma import prisma
from src.utils.security import hash_password, verify_password
from src.utils.jwt import create_access_token, create_refresh_token
from src.models.user import UserCreate, LoginSchema, User
from datetime import datetime
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth, OAuthError
from src.core.config import settings
# from src.models.user import UserOut, LoginSchema

auth_router = APIRouter()

oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://www.googleapis.com/oauth2/v1/userinfo',
    client_kwargs={
        'scope': 'openid email profile',
        'redirect_url': settings.GOOGLE_REDIRECT_URI
    },
)


@auth_router.get("/google")
async def google_login(request: Request):
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)


@auth_router.get("/google/callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    email = user_info.get("email")
    if not email:
        raise HTTPException(400, "Email not provided by Google")


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
