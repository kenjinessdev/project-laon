# routes/auth.py
from fastapi import APIRouter, Depends
from src.dependencies.auth import require_role

customer_route = APIRouter()


@customer_route.get("/dashboard")
async def farmer_dashboard(user=Depends(require_role("customer"))):
    return {"message": f"Welcome, Customer {user.first_name}"}
