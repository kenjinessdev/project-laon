# routes/auth.py
from fastapi import APIRouter, Depends
from src.dependencies.auth import require_role

farmer_router = APIRouter()


@farmer_router.get("/dashboard")
async def farmer_dashboard(user=Depends(require_role("farmer"))):
    return {"message": f"Welcome, Farmer {user.first_name}"}
