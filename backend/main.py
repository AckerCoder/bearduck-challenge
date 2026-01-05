from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
import uuid

from database import engine, get_db, Base
import models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schemas
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: str

    class Config:
        from_attributes = True

class CartItemBase(BaseModel):
    product_id: str
    quantity: int

class CartItem(CartItemBase):
    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    items: List[CartItem]

class OrderItemBase(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    price: float

class OrderItem(OrderItemBase):
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: str
    items: List[OrderItem]
    total: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class CreateOrderRequest(BaseModel):
    cart_items: List[CartItem]

# Initialize sample products
def init_products(db: Session):
    """Initialize database with sample products if empty"""
    count = db.query(models.Product).count()
    if count > 0:
        return

    sample_products = [
        models.Product(
            id=str(uuid.uuid4()),
            name="Wireless Headphones",
            description="High-quality wireless headphones with noise cancellation",
            price=99.99,
            stock=50,
            image_url="https://i.imgur.com/ZANVnHE.jpg"
        ),
        models.Product(
            id=str(uuid.uuid4()),
            name="Smart Watch",
            description="Fitness tracker with heart rate monitor",
            price=199.99,
            stock=30,
            image_url="https://i.imgur.com/mp3rUty.jpg"
        ),
        models.Product(
            id=str(uuid.uuid4()),
            name="Laptop Backpack",
            description="Water resistant laptop backpack with USB charging port",
            price=49.99,
            stock=100,
            image_url="https://i.imgur.com/9DqEOV5.jpg"
        ),
        models.Product(
            id=str(uuid.uuid4()),
            name="Running Shoes",
            description="Comfortable running shoes with excellent cushioning",
            price=89.99,
            stock=75,
            image_url="https://i.imgur.com/tXeOYWE.jpg"
        ),
        models.Product(
            id=str(uuid.uuid4()),
            name="Mechanical Keyboard",
            description="RGB mechanical keyboard with blue switches",
            price=129.99,
            stock=40,
            image_url="https://i.imgur.com/R3iobJA.jpg"
        ),
        models.Product(
            id=str(uuid.uuid4()),
            name="Wireless Mouse",
            description="Ergonomic wireless mouse with precision tracking",
            price=29.99,
            stock=120,
            image_url="https://i.imgur.com/w3Y8NwQ.jpg"
        ),
    ]

    db.add_all(sample_products)
    db.commit()

@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    init_products(db)
    db.close()

# Product endpoints
@app.get("/api/products", response_model=List[Product])
def get_products(db: Session = Depends(get_db)):
    """Get all products"""
    products = db.query(models.Product).all()
    return products

@app.get("/api/products/{product_id}", response_model=Product)
def get_product(product_id: str, db: Session = Depends(get_db)):
    """Get a single product by ID"""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/products", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product (for admin/testing)"""
    db_product = models.Product(
        id=str(uuid.uuid4()),
        **product.dict()
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Cart endpoints
def get_or_create_cart(session_id: str, db: Session) -> models.Cart:
    """Get or create cart for session"""
    cart = db.query(models.Cart).filter(models.Cart.session_id == session_id).first()
    if not cart:
        cart = models.Cart(session_id=session_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

@app.get("/api/cart/{session_id}", response_model=CartResponse)
def get_cart(session_id: str, db: Session = Depends(get_db)):
    """Get cart for a session"""
    cart = get_or_create_cart(session_id, db)
    items = [{"product_id": item.product_id, "quantity": item.quantity}
             for item in cart.items]
    return {"items": items}

@app.post("/api/cart/{session_id}/items")
def add_to_cart(session_id: str, cart_item: CartItemBase, db: Session = Depends(get_db)):
    """Add item to cart"""
    # Verify product exists and has stock
    product = db.query(models.Product).filter(models.Product.id == cart_item.product_id).first()
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

@app.put("/api/cart/{session_id}/items/{product_id}")
def update_cart_item(
    session_id: str,
    product_id: str,
    cart_item: CartItemBase,
    db: Session = Depends(get_db)
):
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

@app.delete("/api/cart/{session_id}/items/{product_id}")
def remove_from_cart(session_id: str, product_id: str, db: Session = Depends(get_db)):
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

@app.delete("/api/cart/{session_id}")
def clear_cart(session_id: str, db: Session = Depends(get_db)):
    """Clear entire cart"""
    cart = get_or_create_cart(session_id, db)

    # Delete all cart items
    db.query(models.CartItem).filter(models.CartItem.cart_id == cart.id).delete()
    db.commit()

    return {"message": "Cart cleared"}

# Order endpoints
@app.post("/api/orders", response_model=OrderResponse)
def create_order(order_request: CreateOrderRequest, db: Session = Depends(get_db)):
    """Create an order from cart items"""
    if not order_request.cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    order_items = []
    total = 0.0

    # Validate and process each item
    for cart_item in order_request.cart_items:
        product = db.query(models.Product).filter(
            models.Product.id == cart_item.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {cart_item.product_id} not found"
            )

        if product.stock < cart_item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}"
            )

        # Deduct stock
        product.stock -= cart_item.quantity

        # Create order item
        order_item = models.OrderItem(
            product_id=product.id,
            product_name=product.name,
            quantity=cart_item.quantity,
            price=product.price
        )
        order_items.append(order_item)
        total += product.price * cart_item.quantity

    # Create order
    order = models.Order(
        id=str(uuid.uuid4()),
        total=round(total, 2),
        status="pending",
        items=order_items
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order

@app.get("/api/orders", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    """Get all orders"""
    orders = db.query(models.Order).order_by(models.Order.created_at.desc()).all()
    return orders

@app.get("/api/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    """Get a single order by ID"""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/")
def root():
    return {"message": "E-commerce API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
