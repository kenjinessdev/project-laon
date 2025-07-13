from fastapi import Request, APIRouter, HTTPException, Response
from src.db.prisma import prisma
from datetime import datetime
from src.core.config import settings
from src.core.limiter import limiter
from src.utils.jwt import create_access_token, create_refresh_token
from src.core.oauth import oauth
from jose import JWTError

facebook_router = APIRouter()

oauth.register(
    name='facebook',
    client_id=settings.FACEBOOK_CLIENT_ID,
    client_secret=settings.FACEBOOK_CLIENT_SECRET,
    access_token_url='https://graph.facebook.com/v19.0/oauth/access_token',
    authorize_url='https://www.facebook.com/v19.0/dialog/oauth',
    api_base_url='https://graph.facebook.com/v19.0/',
    client_kwargs={
        'scope': 'email public_profile user_birthday user_gender'
    },
)


@facebook_router.get("/facebook")
async def facebook_login(request: Request):
    redirect_uri = settings.FACEBOOK_REDIRECT_URI
    return await oauth.facebook.authorize_redirect(request, redirect_uri)


@facebook_router.get("/facebook/callback")
@limiter.limit("10/minute")
async def facebook_callback(request: Request, response: Response):
    try:
        token = await oauth.facebook.authorize_access_token(request)

        resp = await oauth.facebook.get(
            "me?fields=id,name,email,picture,birthday,gender",
            token=token
        )
        profile = resp.json()

        email = profile.get("email")
        name = profile.get("name", "")
        picture = profile.get("picture", {}).get("data", {}).get("url", "")
        birthday_str = profile.get("birthday")  # Expected format: MM/DD/YYYY
        gender = profile.get("gender", "unspecified").lower()

        if not email:
            raise HTTPException(400, "Email not provided by Facebook")

        user = await prisma.user.find_unique(where={"email": email})
        if not user:
            # Split full name
            first_name, *last_parts = name.split(" ")
            last_name = " ".join(last_parts) if last_parts else ""
            role = request.session.get("role", "customer")

            # Parse birthday string
            try:
                birthday = datetime.strptime(
                    birthday_str, "%m/%d/%Y") if birthday_str else datetime(2000, 1, 1)
            except Exception:
                birthday = datetime(2000, 1, 1)

            user = await prisma.user.create(data={
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "profile_image_url": picture,
                "password": "",
                "role": role,
                "birthday": birthday,
                "gender": gender,
                "middle_name": "",
                "suffix": "",
                "phone_number": None
            })

        # 🔐 Token issuance
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        # 🍪 Store refresh token in HttpOnly cookie
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

    except Exception as e:
        raise HTTPException(400, detail=f"Facebook login failed: {str(e)}")
