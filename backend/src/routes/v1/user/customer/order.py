from fastapi import APIRouter, Depends, HTTPException
from src.dependencies.auth import require_role
from src.db.prisma import prisma
from src.models.user import User
from src.models.cart import Cart, AddToCartRequest, UpdateQuantityRequest

customer_order_route = APIRouter()

customer_role = require_role("customer")
