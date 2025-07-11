from fastapi import APIRouter
from src.routes.v1 import v1_router

router = APIRouter()

router.include_router(v1_router, prefix="/api/v1")


@router.get("/")
def read_root():
    return {
        "LAON-API": "Welcome",
    }
