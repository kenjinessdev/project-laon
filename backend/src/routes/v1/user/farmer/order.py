from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request
)
from fastapi.encoders import jsonable_encoder
from src.dependencies.auth import require_role
from src.db.prisma import prisma
from src.models.user import User
from src.core.limiter import limiter
from src.models.query_params import OrderQueryParamsStatus
from src.models.order import OrderStatusUpdate
from src.routes.v1.realtime.notification import _send_notification

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


@farmer_order_route.patch("/orders/{order_id}/status")
async def update_product_status(
    order_id: int,
    payload: OrderStatusUpdate,
    current_user: User = Depends(farmer_role),
):
    status = payload.status.lower()

    if status not in ["preparing", "ready_to_ship", "delivered", "cancelled", "rejected", "shipped"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid status. Allowed values: preparing, ready_to_ship, delivered, cancelled, rejected, shipped"
        )

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

    if farmer_order.status == "delivered":
        raise HTTPException(
            status_code=400,
            detail="Order already delivered. Cannot change status."
        )

    if farmer_order.status == "cancelled":
        raise HTTPException(
            status_code=400,
            detail="Order already cancelled. Cannot change status."
        )
    if farmer_order.status == "rejected":
        raise HTTPException(
            status_code=400,
            detail="Order already rejected. Cannot change status."
        )
    if farmer_order.status == "ready_to_ship" and status != "delivered":
        raise HTTPException(
            status_code=400,
            detail="Order is ready to ship. Cannot change status to anything other than delivered."
        )

    if farmer_order.status == "preparing" and status not in ["ready_to_ship", "cancelled", "rejected"]:
        raise HTTPException(
            status_code=400,
            detail="Order is preparing. Cannot change status to anything other than ready_to_ship, cancelled, or rejected."
        )

    # add shipped
    if farmer_order.status == "preparing" and status == "shipped":
        raise HTTPException(
            status_code=400,
            detail="Order is preparing. Cannot change status to shipped directly."
        )

    if farmer_order.status == "preparing" and status == "delivered":
        raise HTTPException(
            status_code=400,
            detail="Order is preparing. Cannot change status to delivered directly."
        )

    if farmer_order.status == "ready_to_ship" and status not in ["delivered", "cancelled", "rejected"]:
        raise HTTPException(
            status_code=400,
            detail="Order is ready to ship. Cannot change status to anything other than delivered, cancelled, or rejected."
        )

    if farmer_order.status == "delivered" and status != "delivered":
        raise HTTPException(
            status_code=400,
            detail="Order is already delivered. Cannot change status."
        )

    if farmer_order.status == "cancelled" and status != "cancelled":
        raise HTTPException(
            status_code=400,
            detail="Order is already cancelled. Cannot change status."
        )

    if farmer_order.status == "rejected" and status != "rejected":
        raise HTTPException(
            status_code=400,
            detail="Order is already rejected. Cannot change status."
        )

    updated_order = await prisma.farmerorder.update(
        where={"id": order_id},
        data={"status": status},
        include={
            "order": {
                "include": {
                    "customer": True,
                }
            }
        }
    )

    if updated_order.status == "shipped":
        payload = {
            "title": "Your order has been shipped",
            "message":
            f"Your order with ID {updated_order.order.id} has been shipped by {
                current_user.first_name} {current_user.last_name}.",
            "user_id": updated_order.order.customer_id,
            "actor_id": current_user.id,
            "actor_name":
            f"{current_user.first_name} {current_user.last_name}",
            "type": "order_placed",
            "data": {"order_id": str(updated_order.order.id)}
        }
        await _send_notification(payload)

    elif updated_order.status == "delivered":
        payload = {
            "title": "Your order has been delivered",
            "message":
            f"Your order with ID {updated_order.order.id} has been delivered by {
                current_user.first_name} {current_user.last_name}.",
            "user_id": updated_order.order.customer_id,
            "actor_id": current_user.id,
            "actor_name":
            f"{current_user.first_name} {current_user.last_name}",
            "type": "order_delivered",
            "data": {"order_id": str(updated_order.order.id)}
        }
        await _send_notification(payload)
    elif updated_order.status == "cancelled":
        payload = {
            "title": "Your order has been cancelled",
            "message":
            f"Your order with ID {updated_order.order.id} has been cancelled by {
                current_user.first_name} {current_user.last_name}.",
            "user_id": updated_order.order.customer_id,
            "actor_id": current_user.id,
            "actor_name":
            f"{current_user.first_name} {current_user.last_name}",
            "type": "order_cancelled",
            "data": {"order_id": str(updated_order.order.id)}
        }
        await _send_notification(payload)

    return {
        "message": f"Order status updated to {status}",
        "farmer_order": updated_order
    }
