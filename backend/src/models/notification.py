from pydantic import BaseModel
from typing import Optional
from enum import Enum


class NotificationType(str, Enum):
    order_placed = "order_placed"
    product_updated = "product_updated"
    payment_received = "payment_received"
    low_stock = "low_stock"
    order_cancelled = "order_cancelled"
    message_received = "message_received"
    bulk_order_placed = "bulk_order_placed"


class NotificationPayload(BaseModel):
    user_id: str
    actor_id: Optional[str] = None
    actor_name: Optional[str] = None
    title: str
    message: str
    type: NotificationType
    data: Optional[dict] = None
