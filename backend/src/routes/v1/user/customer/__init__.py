from fastapi import APIRouter, Depends, Query
from src.dependencies.auth import require_role
from src.db.prisma import prisma
from src.models.product import Product
from typing import List, Optional

customer_route = APIRouter()

customer_role = require_role("customer")


@customer_route.get("/dashboard")
async def farmer_dashboard(user=Depends(require_role("customer"))):
    return {"message": f"Welcome, Customer {user.first_name}"}


@customer_route.get("/products", response_model=List[Product])
async def get_products(
    skip: int = Query(0, ge=0),
    take: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
):
    filters = {
        "status": "active",
        "visibility": "public",
    }
    if search:
        filters["name"] = {"contains": search, "mode": "insensitive"}
    if category_id:
        filters["category_id"] = category_id
    if min_price and max_price:
        filters["price_per_unit"] = {"gte": min_price, "lte": max_price}

    products = await prisma.product.find_many(
        where=filters,
        skip=skip,
        take=take,
        order={"created_at": "desc"}
    )
    return products
