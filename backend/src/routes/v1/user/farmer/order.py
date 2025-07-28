from fastapi import APIRouter, Depends, HTTPException, Request, Query
from src.dependencies.auth import require_role
from src.db.prisma import prisma
from src.models.user import User
from src.models.cart import Cart, AddToCartRequest, UpdateQuantityRequest
from src.core.limiter import limiter
from collections import defaultdict
from src.models.query_params import OrderQueryParams

farmer_order_route = APIRouter()

farmer_role = require_role("farmer")


@farmer_order_route.get("/orders")
async def orders(
    request: Request,
    current_user: User = Depends(farmer_role),
    params: OrderQueryParams = Depends()

):
    filters = [
        {"farmer_id": current_user.id}
    ]

    if params.search:
        filter.append({
            "status": params.search.lower()
        })

    orders = await prisma.farmerorder.find_many(
        where={"AND": filters},
        skip=params.skip,
        take=params.limit,
        order={"created_at": "desc"}
    )

    total_count = await prisma.farmerorder.count(
        where={"AND": filters}
    )

    return {
        "message": f"{total_count} orders found",
        "total": total_count,
        "skip": params.skip,
        "limit": params.limit,
        "orders": orders
    }
