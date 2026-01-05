"""
Product business logic
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException
import models
import schemas
import uuid


def get_all_products(db: Session):
    """Get all products from database"""
    return db.query(models.Product).all()


def get_product_by_id(product_id: str, db: Session):
    """Get a single product by ID"""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def create_product(product_data: schemas.ProductCreate, db: Session):
    """Create a new product"""
    db_product = models.Product(
        id=str(uuid.uuid4()),
        **product_data.dict()
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def init_sample_products(db: Session):
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
