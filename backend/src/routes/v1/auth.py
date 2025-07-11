# routes/auth.py
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import Request, Response, HTTPException, APIRouter
from src.db.prisma import prisma
from src.utils.security import hash_password, verify_password
from src.utils.jwt import create_access_token, create_refresh_token
from src.models.user import UserCreate, LoginSchema, User
from datetime import datetime
from src.core.config import settings
from prisma.errors import UniqueViolationError
from src.core.limiter import limiter
from jose import JWTError
from src.utils.jwt import decode_token

# from src.models.user import UserOut, LoginSchema

auth_router = APIRouter()

oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',  # ✅ has https://
    userinfo_endpoint='https://www.googleapis.com/oauth2/v1/userinfo',  # ✅ good
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/user.gender.read',
    },
)


@auth_router.get("/google")
async def google_login(request: Request, role: str = "customer"):
    request.session["role"] = role  # store it in session
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)


@auth_router.get("/google/callback", name="google_callback")
@limiter.limit("10/minute")
async def google_callback(request: Request, response: Response):
    try:
        token = await oauth.google.authorize_access_token(request)

        resp = await oauth.google.get(
            "https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses,photos,birthdays,genders,phoneNumbers",
            token=token
        )
        user_info = resp.json()

        # Safe parsing
        names = user_info.get("names", [{}])[0]
        photos = user_info.get("photos", [{}])[0]
        emails = user_info.get("emailAddresses", [{}])[0]
        birthdays = user_info.get("birthdays", [{}])[0]
        genders = user_info.get("genders", [{}])[0]
        phones = user_info.get("phoneNumbers", [{}])[0]

        email = emails.get("value")
        if not email:
            raise HTTPException(400, "Email not provided by Google")

        user = await prisma.user.find_unique(where={"email": email})
        if not user:
            role = request.session.get("role", "customer")

            # Convert birthday to datetime if available
            bdate = birthdays.get("date")
            birthday = datetime(
                year=int(bdate.get("year", 2000)),
                month=int(bdate.get("month", 1)),
                day=int(bdate.get("day", 1))
            ) if bdate else datetime(2000, 1, 1)

            user = await prisma.user.create(data={
                "first_name": names.get("givenName", ""),
                "last_name": names.get("familyName", ""),
                "email": email,
                "profile_image_url": photos.get("url", ""),
                "password": "",
                "role": role,
                "birthday": birthday,
                "gender": genders.get("value", "unspecified").lower(),
                "phone_number": phones.get("value", None),
                "middle_name": "",
                "suffix": ""
            })

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        # 🍪 e HttpOnly refresh token cookie
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=not settings.DEBUG,  # True in production
            samesite="lax",
            max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except OAuthError as e:
        raise HTTPException(status_code=400, detail=f"OAuth error: {str(e)}")


@auth_router.post("/register", response_model=User)
@limiter.limit("5/minute")
async def register(request: Request, user: UserCreate):
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
        return new_user

    except UniqueViolationError:
        raise HTTPException(status_code=400, detail="Email already registered")


@auth_router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, response: Response, creds: LoginSchema):
    user = await prisma.user.find_unique(where={"email": creds.email})
    if not user or not verify_password(creds.password, user.password):
        raise HTTPException(401, "Invalid credentials")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    # ✅ Store refresh token in HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

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
