from fastapi import APIRouter
from src.routes.auth import auth_router
from src.routes.protected import role_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth")
router.include_router(role_router)


@router.get("/")
def read_root():
    return {"Hello": "World"}
