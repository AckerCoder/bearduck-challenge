"""
Order API routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import schemas
from controllers import orders as order_controller


router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("", response_model=schemas.OrderResponse)
def create_order(
    order_request: schemas.CreateOrderRequest,
    db: Session = Depends(get_db)
):
    """Create an order from cart items"""
    return order_controller.create_order(order_request, db)


@router.get("", response_model=List[schemas.OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    """Get all orders"""
    return order_controller.get_all_orders(db)


@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    """Get a single order by ID"""
    return order_controller.get_order_by_id(order_id, db)
