from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from src.routes.routes import router as api_router
from src.db.prisma import prisma
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from src.core.config import settings
from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from src.core.limiter import limiter, rate_limit_handler
from src.core.exception_handlers import validation_exception_handler

app = FastAPI(
    title="LAON"
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET)
app.add_middleware(
    CORSMiddleware,
    # replace allow_origin with react localhost
    allow_origins=["http://localhost:3000"] + settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(settings.ALLOWED_ORIGINS[0])

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(api_router)


@app.on_event("startup")
async def startup():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()
