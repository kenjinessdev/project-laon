from fastapi import APIRouter, Depends
from src.dependencies.auth import require_role
from src.models.product import ProductCreate, Product
from src.db.prisma import prisma

farmer_product_router = APIRouter()


@farmer_product_router.post("/product", response_model=Product)
async def create_product(
    payload: ProductCreate,
    current_user=Depends(require_role("farmer"))
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
