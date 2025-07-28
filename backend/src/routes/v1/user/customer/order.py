from fastapi import Query
from fastapi import APIRouter, Depends, HTTPException, Request
from src.dependencies.auth import require_role
from src.db.prisma import prisma
from src.models.user import User
from src.models.cart import Cart, AddToCartRequest, UpdateQuantityRequest
from src.core.limiter import limiter
from collections import defaultdict

customer_order_route = APIRouter()

customer_role = require_role("customer")


@customer_order_route.post("/checkout")
@limiter.limit("5/minute")
async def checkout(
    request: Request,
    current_user: User = Depends(customer_role)
):
    cart = await prisma.cart.find_first(
        where={
            "AND": [
                {"customer_id": current_user.id},
                {"is_active": True}
            ]
        }
    )

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_items = await prisma.cartitem.find_many(
        where={"cart_id": cart.id},
        include={"product": True}
    )

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = sum(item.product.price_per_unit *
                item.quantity for item in cart_items)

    customer_order = await prisma.customerorder.create(
        data={
            "customer_id": current_user.id,
            "total_price": total,
            "status": "pending",
        }
    )

    farmer_groups = defaultdict(list)

    for item in cart_items:
        farmer_id = item.product.user_id
        farmer_groups[farmer_id].append(item)

    for farmer_id, items in farmer_groups.items():
        subtotal = sum(item.quantity *
                       item.product.price_per_unit for item in items)
        farmer_order = await prisma.farmerorder.create(
            data={
                "customer_order_id": customer_order.id,
                "farmer_id": farmer_id,
                "subtotal": subtotal,
                "status": "pending"
            }
        )

        for item in items:
            await prisma.orderitem.create(
                data={
                    "customer_order_id": customer_order.id,
                    "farmer_order_id": farmer_order.id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": item.product.price_per_unit
                }
            )

    await prisma.cart.update(
        where={"id": cart.id},
        data={"is_active": False}
    )

    return {"message": "Checkout successful", "order": customer_order}


@customer_order_route.get("/orders")
@limiter.limit("10/minute")
async def orders(
    current_user: User = Depends(customer_role),
    search: str = Query(default="", description="Search by status"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1)
):
    filters = [
        {"customer_id": current_user.id}
    ]

    # Filter by status if provided
    if search:
        filters.append({
            "status": search.lower()  # make sure your enum uses uppercase like "PENDING"
        })

    orders = await prisma.customerorder.find_many(
        where={"AND": filters},
        skip=skip,
        take=limit,
        order={"created_at": "desc"}
    )

    total_count = await prisma.customerorder.count(
        where={"AND": filters}
    )

    return {
        "message": f"{total_count} orders found",
        "total": total_count,
        "skip": skip,
        "limit": limit,
        "orders": orders
    }


@customer_order_route.post("/orders/{order_id}/cancel")
@limiter.limit("10/minute")
async def cancel_order(
    order_id: str,
    current_user: User = Depends(customer_role)
):
    order = await prisma.customerorder.find_unique(where={"id": order_id})

    if not order or order.customer_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found")

    updated_order = await prisma.customerorder.update(
        where={"id": order_id},
        data={"status": "cancelled"}
    )

    return {
        "message": "Order cancelled successfully",
        "order": updated_order
    }
