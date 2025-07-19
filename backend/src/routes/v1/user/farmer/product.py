from fastapi import APIRouter, Depends, Request, HTTPException, UploadFile, File, Form, Query
from src.dependencies.auth import require_role
from src.models.product import Product, ProductUpdate
from src.models.user import User
from src.db.prisma import prisma
from src.core.limiter import limiter
from typing import List, Optional
from datetime import datetime
from src.core.config import settings
from decimal import Decimal
import requests
import uuid


farmer_product_router = APIRouter()

farmer_role = require_role("farmer")

product_image_bucket = "product-images"


ALLOWED_ORDER_FIELDS = settings.ORDER_BY_FIELDS


@farmer_product_router.get("/products", response_model=List[Product])
async def my_products(
    name: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    visibility: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    skip: int = Query(0, ge=0),
    take: int = Query(10, ge=1),
    order_by: str = Query("created_at"),
    order: str = Query("desc"),
    current_user: User = Depends(farmer_role)
):
    # Validate `order_by`
    if order_by not in ALLOWED_ORDER_FIELDS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid order_by field. Allowed: {', '.join(ALLOWED_ORDER_FIELDS)}"
        )

    if order.lower() not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order value. Use 'asc' or 'desc'"
        )

    filters = {
        "user_id": current_user.id
    }

    if name:
        filters["name"] = {"contains": name, "mode": "insensitive"}

    if status:
        filters["status"] = status

    if visibility:
        filters["visibility"] = visibility

    if min_price is not None or max_price is not None:
        filters["price_per_unit"] = {}
        if min_price is not None:
            filters["price_per_unit"]["gte"] = min_price
        if max_price is not None:
            filters["price_per_unit"]["lte"] = max_price

    order_clause = {
        order_by: order.lower(),
    }

    products = await prisma.product.find_many(
        where=filters,
        skip=skip,
        take=take,
        order=order_clause,
        include={"images": True}
    )

    return products


@farmer_product_router.get("/product/{product_id}", response_model=Product)
async def view_product(
    product_id: str,
    current_user: User = Depends(farmer_role)
):
    product = await prisma.product.find_first(
        where={'id': product_id},
        include={'images': True}

    )

    if not product or product.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@farmer_product_router.post("/product", response_model=Product)
@limiter.limit("5/minute")
async def create_product(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    unit: str = Form(...),
    price_per_unit: float = Form(...),
    stock_quantity: int = Form(...),
    status: str = Form(...),
    visibility: str = Form(...),
    images: List[UploadFile] = File(None),
    current_user: User = Depends(farmer_role),
):
    # Validate input lengths
    if len(name) > 100:
        raise HTTPException(
            status_code=422, detail="Name must be 100 characters or fewer")
    if len(unit) > 20:
        raise HTTPException(
            status_code=422, detail="Unit must be 20 characters or fewer")

    # Create the product
    product = await prisma.product.create(data={
        'user_id': current_user.id,
        'name': name,
        'description': description,
        'unit': unit,
        'category_id': None,
        'price_per_unit': price_per_unit,
        'stock_quantity': stock_quantity,
        'status': status,
        'visibility': visibility
    })

    # Upload multiple images
    if images:
        for image in images:
            try:
                filename = f"{uuid.uuid4()}_{image.filename}"
                content = await image.read()

                upload_url = f"{settings.SUPABASE_URL}/storage/v1/object/{product_image_bucket}/{filename}"
                headers = {
                    "Authorization": f"Bearer {settings.SUPABASE_SERVICE_KEY}",
                    "Content-Type": image.content_type
                }

                response = requests.post(
                    upload_url, headers=headers, data=content)

                if response.status_code != 200:
                    raise Exception("Image upload failed")

                public_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{product_image_bucket}/{filename}"

                await prisma.productimage.create(data={
                    "product_id": product.id,
                    "image_public_url": public_url,
                })

            except Exception:
                await prisma.product.delete(where={"id": product.id})
                raise HTTPException(
                    status_code=500, detail="One or more images failed to upload")

    # Fetch product with images
    updated_product = await prisma.product.find_unique(
        where={"id": product.id},
        include={"images": True}
    )

    return updated_product


@farmer_product_router.put("/product/{product_id}", response_model=Product)
@limiter.limit("5/minute")
async def update_product(
    request: Request,
    product_id: str,
    updated_product: ProductUpdate,
    current_user: User = Depends(farmer_role)
):
    product = await prisma.product.find_unique(where={"id": product_id})

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
    product = await prisma.product.find_unique(where={"id": product_id})

    if not product or product.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Product not found")

    product = await prisma.product.delete(where={'id': product_id})
    return {'detail': 'Product deleted successfully'}


@farmer_product_router.post("/product/{product_id}/images", response_model=Product)
async def upload_product_image(
    product_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(farmer_role)
):
    product = await prisma.product.find_unique(where={"id": product_id})

    if not product or product.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Product not found")

    filename = f"{uuid.uuid4()}_{file.filename}"
    file_content = await file.read()

    upload_url = f"{settings.SUPABASE_URL}/storage/v1/object/{product_image_bucket}/{filename}"
    headers = {
        "Authorization": f"Bearer {settings.SUPABASE_SERVICE_KEY}",
        "Content-Type": file.content_type
    }

    response = requests.post(upload_url, headers=headers, data=file_content)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Upload failed")

    public_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{product_image_bucket}/{filename}"

    await prisma.productimage.create(data={
        "product_id": product.id,
        "image_public_url": public_url,
    })

    return {"detail": "Image uploaded successfully"}


@farmer_product_router.delete("/product/{product_id}/images/{image_id}")
async def delete_product_image(
    product_id: str,
    image_id: str,
    current_user: User = Depends(farmer_role)
):
    # Find product and its images
    product = await prisma.product.find_unique(where={"id": product_id})

    if not product or product.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Product not found")

    # Find the image record by image_id
    image = await prisma.productimage.find_unique(where={"id": image_id})

    if not image or image.product_id != product_id:
        raise HTTPException(status_code=404, detail="Image not found")

    # Extract just the filename from the public URL
    # Assuming the format: https://your-project.supabase.co/storage/v1/object/public/product-images/{filename}
    try:
        filename = image.image_public_url.split("/")[-1]
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image URL")

    # Delete image from Supabase Storage
    file_path = f"{product_image_bucket}/{filename}"
    delete_url = f"{settings.SUPABASE_URL}/storage/v1/object/{file_path}"
    headers = {
        "Authorization": f"Bearer {settings.SUPABASE_SERVICE_KEY}"
    }

    response = requests.delete(delete_url, headers=headers)
    if response.status_code not in [200, 204, 404]:
        raise HTTPException(
            status_code=500, detail="Failed to delete image from Supabase")

    # Delete image record from database
    await prisma.productimage.delete(where={"id": image_id})

    return {"detail": "Image deleted successfully"}
