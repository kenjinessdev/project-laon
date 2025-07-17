from fastapi import APIRouter, Depends, Request, HTTPException
from src.dependencies.auth import require_role
from src.models.product import ProductCreate, Product, ProductUpdate
from src.models.user import User
from src.db.prisma import prisma
from src.core.limiter import limiter
from typing import List
from datetime import datetime

farmer_product_router = APIRouter()

farmer_role = require_role("farmer")


@farmer_product_router.get("/products", response_model=List[Product])
async def my_products(
    current_user: User = Depends(farmer_role)
):
    products = await prisma.product.find_many(
        where={
            'user_id': current_user.id
        }
    )

    return products


@farmer_product_router.post("/product", response_model=Product)
@limiter.limit("5/minute")
async def create_product(
    request: Request,
    payload: ProductCreate,
    current_user: User = Depends(farmer_role)
):
    product = await prisma.product.create(data={
        'user_id': current_user.id,
        'name': payload.name,
        'description': payload.description,
        'unit': payload.unit,
        'category_id': None,
        'price_per_unit': payload.price_per_unit,
        'stock_quantity': payload.stock_quantity,
        'status': payload.status,
        'visibility': payload.visibility
    })

    return product


@farmer_product_router.put("/product/{product_id}", response_model=Product)
@limiter.limit("5/minute")
async def update_product(
    request: Request,
    product_id: str,
    updated_product: ProductUpdate,
    current_user: User = Depends(farmer_role)
):
    product = await prisma.product.find_unique(
        where={"id": product_id},
        include={"user": True}
    )
    if not product or product.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Product not found")

    updated_data = updated_product.dict(exclude_unset=True)
    updated_data['updated_at'] = datetime.utcnow()
    product = await prisma.product.update(
        where={'id': product_id},
        data=updated_data
    )

    return product


@farmer_product_router.delete("/product/{product_id}")
async def delete_product(
    request: Request,
    product_id: str,
    current_user: User = Depends(farmer_role)
):
    print("Current User ID:", current_user.id)
    product = await prisma.product.find_unique(
        where={"id": product_id},
        include={"user": True}
    )

    if not product or product.user.id != current_user.id:
        raise HTTPException(status_code=404, detail="Product not found")

    product = await prisma.product.delete(where={'id': product_id})
    return {'detail': 'Product deleted successfully'}
