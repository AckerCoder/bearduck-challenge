"""
Shopping cart business logic
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException
import models
import schemas


def get_or_create_cart(session_id: str, db: Session) -> models.Cart:
    """Get or create cart for session"""
    cart = db.query(models.Cart).filter(models.Cart.session_id == session_id).first()
    if not cart:
        cart = models.Cart(session_id=session_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


def get_cart(session_id: str, db: Session):
    """Get cart items for a session"""
    cart = get_or_create_cart(session_id, db)
    items = [{"product_id": item.product_id, "quantity": item.quantity}
             for item in cart.items]
    return {"items": items}


def add_item_to_cart(session_id: str, cart_item: schemas.CartItemBase, db: Session):
    """Add item to cart"""
    # Verify product exists and has stock
    product = db.query(models.Product).filter(
        models.Product.id == cart_item.product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock < cart_item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    cart = get_or_create_cart(session_id, db)

    # Check if item already in cart
    existing_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.id,
        models.CartItem.product_id == cart_item.product_id
    ).first()

    if existing_item:
        new_quantity = existing_item.quantity + cart_item.quantity
        if product.stock < new_quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        existing_item.quantity = new_quantity
    else:
        new_item = models.CartItem(
            cart_id=cart.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity
        )
        db.add(new_item)

    db.commit()

    items = [{"product_id": item.product_id, "quantity": item.quantity}
             for item in cart.items]
    return {"message": "Item added to cart", "cart": {"items": items}}


def update_cart_item(session_id: str, product_id: str, cart_item: schemas.CartItemBase, db: Session):
    """Update cart item quantity"""
    cart = get_or_create_cart(session_id, db)

    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock < cart_item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.id,
        models.CartItem.product_id == product_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not in cart")

    item.quantity = cart_item.quantity
    db.commit()

    items = [{"product_id": i.product_id, "quantity": i.quantity}
             for i in cart.items]
    return {"message": "Cart updated", "cart": {"items": items}}


def remove_item_from_cart(session_id: str, product_id: str, db: Session):
    """Remove item from cart"""
    cart = get_or_create_cart(session_id, db)

    item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.id,
        models.CartItem.product_id == product_id
    ).first()

    if item:
        db.delete(item)
        db.commit()

    items = [{"product_id": i.product_id, "quantity": i.quantity}
             for i in cart.items]
    return {"message": "Item removed from cart", "cart": {"items": items}}


def clear_cart(session_id: str, db: Session):
    """Clear entire cart"""
    cart = get_or_create_cart(session_id, db)

    # Delete all cart items
    db.query(models.CartItem).filter(models.CartItem.cart_id == cart.id).delete()
    db.commit()

    return {"message": "Cart cleared"}
