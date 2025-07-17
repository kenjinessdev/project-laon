from fastapi import APIRouter, Depends
from src.dependencies.auth import require_role
from src.routes.v1.user.farmer.product import farmer_product_router

farmer_router = APIRouter()
farmer_router.include_router(farmer_product_router)


@farmer_router.get("/dashboard")
async def farmer_dashboard(user=Depends(require_role("farmer"))):
    return {"message": f"Welcome, Farmer {user.first_name}"}
