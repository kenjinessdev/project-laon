from fastapi import APIRouter, Depends
from src.dependencies.auth import require_role
from src.routes.v1.user.customer.cart import customer_cart_route

customer_route = APIRouter()

customer_role = require_role("customer")

customer_route.include_router(customer_cart_route)


@customer_route.get("/dashboard")
async def farmer_dashboard(user=Depends(require_role("customer"))):
    return {"message": f"Welcome, Customer {user.first_name}"}
