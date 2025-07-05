from fastapi import APIRouter
from src.models.user import UserResponse

router = APIRouter()


@router.get("/health", response_model=UserResponse)
async def health_check():
    return {"username": "test_user", "email": "test@example.com"}


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
