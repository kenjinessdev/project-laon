from fastapi import APIRouter, Depends, HTTPException, Request
from src.dependencies.auth import require_role
from src.db.prisma import prisma
from src.models.user import User
from src.models.cart import Cart, AddToCartRequest, UpdateQuantityRequest
from src.core.limiter import limiter
from uuid import UUID

customer_cart_route = APIRouter()

customer_role = require_role("customer")


@customer_cart_route.post("/add-to-cart", response_model=Cart)
@limiter.limit("10/minute")
async def add_to_cart(
    request: Request,
    payload: AddToCartRequest,
    current_user: User = Depends(customer_role)
):
    if payload.quantity <= 0:
        raise HTTPException(
            status_code=400, detail="Quantity must be greater than 0")

    cart = await prisma.cart.find_first(
        where={
            "AND": [
                {"customer_id": current_user.id},
                {"is_active": True}
            ]
        }
    )

    if not cart:

        cart = await prisma.cart.create(data={
            "customer_id": current_user.id,
            "is_active": True
        })

        if not cart:
            raise HTTPException(
                status_code=500, detail="Failed to create cart")

    product = await prisma.product.find_unique(
        where={
            "id": payload.product_id
        }
    )

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # check if the product is already in the cart
    existing_item = await prisma.cartitem.find_first(
        where={
            "AND": [
                {"cart_id": cart.id},
                {"product_id": product.id}
            ]
        }
    )

    # if already in cart
    if existing_item:
        # Update quantity
        await prisma.cartitem.update(
            where={"id": existing_item.id},
            data={"quantity": existing_item.quantity + payload.quantity}
        )

    else:
        # add new item
        await prisma.cartitem.create(
            data={
                "cart_id": cart.id,
                "quantity": payload.quantity,
                "product_id": product.id
            }
        )

    cart = await prisma.cart.find_unique(
        where={"id": cart.id},
        include={
            "customer": True,
            "cart_items": {
                "include": {
                    "product": {
                        "include": {
                            "images": True
                        }
                    }
                }
            }
        }
    )

    return cart


@customer_cart_route.patch("/cart-items/{item_id}/quantity")
@limiter.limit("20/minute")
async def update_cart_item_quantity(
    request: Request,
    item_id: UUID,
    payload: UpdateQuantityRequest,
    current_user: User = Depends(customer_role)
):

    cart_item = await prisma.cartitem.find_unique(
        where={"id": str(item_id)},
        include={"cart": True}
    )
    if not cart_item or cart_item.cart.customer_id != current_user.id:
        raise HTTPException(status_code=404, detail="Cart item not found")

    updated_item = await prisma.cartitem.update(
        where={"id": str(item_id)},
        data={"quantity": payload.quantity}
    )

    return updated_item


@customer_cart_route.delete("/cart-items/{item_id}/delete")
@limiter.limit("10/minute")
async def delete_cart_item(
    request: Request,
    item_id: UUID,
    current_user: User = Depends(customer_role)
):

    cart_item = await prisma.cartitem.find_unique(
        where={"id": str(item_id)},
        include={"cart": True}
    )

    if not cart_item or cart_item.cart.customer_id != current_user.id:
        raise HTTPException(status_code=404, detail="Cart item not found")

    await prisma.cartitem.delete(where={"id": str(item_id)})

    return {"message": "Cart item deleted successfully"}


@customer_cart_route.get("/cart")
@limiter.limit("60/minute")
async def get_cart(
    request: Request,
    current_user: User = Depends(customer_role)
):
    cart = await prisma.cart.find_first(
        where={
            "AND": [
                {"customer_id": current_user.id},
                {"is_active": True}
            ]
        },
        include={
            "cart_items": {
                "include": {
                    "product": {
                        "include": {
                            "images": True
                        }
                    }
                }
            }
        }
    )

    if not cart:
        return {"message": "No active cart found"}

    return {
        "Message": "Active cart found",
        "cart_items_count": len(cart.cart_items),
        "cart": cart
    }
