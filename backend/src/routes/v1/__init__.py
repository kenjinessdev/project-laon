from fastapi import APIRouter
from src.routes.v1.auth import auth_router
from src.routes.v1.user.farmer import farmer_router
from src.routes.v1.user.customer import customer_route
from src.routes.v1.user.user import user_router
from src.routes.v1.user.common.product import product_router
from src.routes.v1.realtime.notification import router as notification_router

v1_router = APIRouter()

v1_router.include_router(auth_router, prefix="/auth")
v1_router.include_router(farmer_router, prefix="/farmer")
v1_router.include_router(customer_route, prefix="/customer")
v1_router.include_router(user_router, prefix="/users")
v1_router.include_router(product_router)
v1_router.include_router(notification_router)


@v1_router.get("/")
def v1():
    return {"message": "Welcome to laon version 1"}
