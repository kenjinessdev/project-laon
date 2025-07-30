from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Query
)
from fastapi.encoders import jsonable_encoder
from src.dependencies.auth import require_role
from src.db.prisma import prisma
from src.models.user import User
from src.models.cart import Cart, AddToCartRequest, UpdateQuantityRequest
from src.core.limiter import limiter
from collections import defaultdict
from src.models.query_params import OrderQueryParams, OrderQueryParamsStatus
from uuid import UUID

farmer_order_route = APIRouter()

farmer_role = require_role("farmer")


@farmer_order_route.get("/orders")
async def orders(
    request: Request,
    current_user: User = Depends(farmer_role),
    params: OrderQueryParamsStatus = Depends()

):
    filters = [
        {"farmer_id": current_user.id}
    ]

    if params.status:
        filters.append({
            "status": params.status.lower()
        })

    orders = await prisma.farmerorder.find_many(
        where={"AND": filters},
        skip=params.skip,
        take=params.limit,
        include={
            "order_item": True,
            "order": {
                "include": {"customer": True}
            }
        },
        order={"created_at": "desc"}
    )

    total_count = await prisma.farmerorder.count(
        where={"AND": filters}
    )

    return {
        "message": f"{total_count} orders found",
        "params": params,
        "total": total_count,
        "skip": params.skip,
        "limit": params.limit,
        "orders": orders
    }


@farmer_order_route.post("/orders/{order_id}/accept")
async def accept_order(
    order_id: int,
    current_user: User = Depends(farmer_role)
):
    farmer_order = await prisma.farmerorder.find_first(
        where={"id": order_id, "farmer_id": current_user.id},
        include={
            "order": {
                "include": {
                    "customer": True,
                }
            }
        }
    )

    if not farmer_order:
        raise HTTPException(status_code=404, detail="Order not found")

    if farmer_order.order.status != "paid":
        raise HTTPException(
            status_code=400,
            detail=jsonable_encoder({
                "error": "Order cannot be accepted",
                "current_status": farmer_order.order.status,
                "allowed_statuses": ["paid"],
                "order": farmer_order.order
            }))

    updated_order = await prisma.farmerorder.update(
        where={"id": order_id},
        data={"status": "preparing"}
    )

    return {
        "message": "Order accepted successfully",
        "order": updated_order
    }
