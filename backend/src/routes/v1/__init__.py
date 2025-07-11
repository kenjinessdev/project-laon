from fastapi import APIRouter
from src.routes.v1.auth import auth_router
from src.routes.v1.farmer import farmer_router
from src.routes.v1.customer import customer_route

v1_router = APIRouter()

v1_router.include_router(auth_router, prefix="/auth")
v1_router.include_router(farmer_router, prefix="/farmer")
v1_router.include_router(customer_route, prefix="/customer")
