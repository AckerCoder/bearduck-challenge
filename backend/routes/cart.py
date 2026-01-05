"""
Shopping cart API routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
import schemas
from controllers import cart as cart_controller


router = APIRouter(prefix="/api/cart", tags=["cart"])


@router.get("/{session_id}", response_model=schemas.CartResponse)
def get_cart(session_id: str, db: Session = Depends(get_db)):
    """Get cart for a session"""
    return cart_controller.get_cart(session_id, db)


@router.post("/{session_id}/items")
def add_to_cart(
    session_id: str,
    cart_item: schemas.CartItemBase,
    db: Session = Depends(get_db)
):
    """Add item to cart"""
    return cart_controller.add_item_to_cart(session_id, cart_item, db)


@router.put("/{session_id}/items/{product_id}")
def update_cart_item(
    session_id: str,
    product_id: str,
    cart_item: schemas.CartItemBase,
    db: Session = Depends(get_db)
):
    """Update cart item quantity"""
    return cart_controller.update_cart_item(session_id, product_id, cart_item, db)


@router.delete("/{session_id}/items/{product_id}")
def remove_from_cart(session_id: str, product_id: str, db: Session = Depends(get_db)):
    """Remove item from cart"""
    return cart_controller.remove_item_from_cart(session_id, product_id, db)


@router.delete("/{session_id}")
def clear_cart(session_id: str, db: Session = Depends(get_db)):
    """Clear entire cart"""
    return cart_controller.clear_cart(session_id, db)
