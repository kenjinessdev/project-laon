from pydantic import BaseModel, constr, condecimal, UUID4
from typing import Optional, Any
from enum import Enum
from datetime import datetime


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
    price_per_unit: float
    stock_quantity: int
    status: ProductStatus = ProductStatus.active
    visibility: Visibility = Visibility.public
    user: Optional[Any] = None
    images: Optional[Any] = None
    reviews: Optional[Any] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[constr(max_length=100)] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    unit: Optional[constr(max_length=20)] = None
    price_per_unit: Optional[float] = None
    stock_quantity: Optional[int] = None
    status: Optional[ProductStatus] = None
    visibility: Optional[Visibility] = None


class Product(ProductBase):
    id: str
    user_id: str
    updated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
