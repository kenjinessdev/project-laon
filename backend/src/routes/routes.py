from fastapi import APIRouter
from src.routes.auth import auth_router
from src.routes.farmer import farmer_router
from src.routes.customer import customer_route

router = APIRouter()

router.include_router(auth_router, prefix="/auth")
router.include_router(farmer_router, prefix="/farmer")
router.include_router(customer_route, prefix="/customer")


@router.get("/")
def read_root():
    return {"Hello": "World"}
