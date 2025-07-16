from pydantic import BaseModel, constr, condecimal, UUID4
from typing import Optional
from enum import Enum


class ProductStatus(str, Enum):
    draft = "draft"
    active = "active"
    archived = "archived"
    sold = "sold"


class Visibility(str, Enum):
    public = "public"
    private = "private"
    admin_only = "admin_only"


class ProductBase(BaseModel):
    name: constr(max_length=100)
    description: str
    category_id: Optional[int] = None
    unit: constr(max_length=20)
    price_per_unit: condecimal(max_digits=12, decimal_places=2)
    stock_quantity: int
    status: ProductStatus = ProductStatus.active
    visibility: Visibility = Visibility.public


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[constr(max_length=100)] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    unit: Optional[constr(max_length=20)] = None
    price_per_unit: Optional[condecimal(
        max_digits=12, decimal_places=2)] = None
    stock_quantity: Optional[int] = None


class Product(ProductBase):
    id: UUID4
    user_id: UUID4

    class Config:
        from_attributes = True
