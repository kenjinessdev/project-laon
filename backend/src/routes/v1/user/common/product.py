from fastapi import Query, APIRouter, HTTPException
from typing import Optional, List
from src.db.prisma import prisma
from src.models.product import Product
from src.core.config import settings

product_router = APIRouter()


@product_router.get("/products")
async def get_products(
    skip: int = Query(0, ge=0),
    take: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    order_by: str = Query("created_at"),
    order: str = Query("desc")
):
    if order_by not in settings.ORDER_BY_FIELDS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid order_by field. Allowed: {', '.join(settings.ORDER_BY_FIELDS)}"
        )

    if order.lower() not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order value. Use 'asc' or 'desc'"
        )

    filters = {
        "status": "active",
        "visibility": "public",
    }

    # Search logic
    if search:
        filters["OR"] = [
            {"name": {"contains": search, "mode": "insensitive"}},
            {"description": {"contains": search, "mode": "insensitive"}},
        ]

    # Price filter
    price_filter = {}
    if min_price is not None:
        price_filter["gte"] = min_price
    if max_price is not None:
        price_filter["lte"] = max_price
    if price_filter:
        filters["price_per_unit"] = price_filter

    # Get total count
    total = await prisma.product.count(where=filters)
    products = await prisma.product.find_many(
        where=filters,
        skip=skip,
        take=take,
        order={order_by: order.lower()}
    )
    return {
        "data": products,
        "total": total,
        "skip": skip,
        "take": take
    }
