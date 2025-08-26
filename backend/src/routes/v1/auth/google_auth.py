from authlib.integrations.starlette_client import OAuthError
from fastapi import Request, Response, HTTPException, APIRouter
from src.db.prisma import prisma
from src.utils.jwt import create_access_token, create_refresh_token, issue_tokens
from datetime import datetime
from src.core.config import settings
from src.core.limiter import limiter
from src.core.oauth import oauth
from src.models.user import OAuthenticatedUser


google_router = APIRouter()

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


@google_router.get("/google")
async def google_login(request: Request, role: str = "customer"):
    request.session["role"] = role
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)


@google_router.get(
    "/google/callback",
    name="google_callback",
    response_model=OAuthenticatedUser
)
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

        access_token = issue_tokens(user.id, response)

        return {
            "access_token": access_token,
            "user": user,
            "token_type": "bearer"
        }

    except OAuthError as e:
        raise HTTPException(status_code=400, detail=f"OAuth error: {str(e)}")
