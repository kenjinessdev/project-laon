from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, Any, List
from src.models.user import User


# CartItems ----------------------
class CartItemBase(BaseModel):
    cart_id: str
    quantity: int
    product_id: str
    product: Optional[Any] = None


class CartItemCreate(CartItemBase):
    pass


class CartItem(CartItemBase):
    id: str
    added_at: datetime


# Cart ---------------------------
class CartBase(BaseModel):
    is_active: bool


class AddToCartRequest(BaseModel):
    product_id: str
    quantity: int = Field(gt=0, description="Quantity must be greater than 0")

    @validator('product_id')
    def validate_uuid(cls, v):
        v = v.replace("-", "")
        if not v:
            raise ValueError("product_id is required")
        if len(v) != 32:
            raise ValueError("product_id must be a 32-character UUID")
        return v


class UpdateQuantityRequest(BaseModel):
    quantity: int = Field(..., gt=0,
                          description="New quantity must be greater than 0")


class Cart(CartBase):
    id: str
    customer_id: str
    created_at: datetime
    updated_at: datetime

    customer: Optional[User] = None
    cart_items: List[CartItem] = []

    class Config:
        from_attributes = True
