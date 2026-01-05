"""
Product API routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import schemas
from controllers import products as product_controller


router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=List[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    """Get all products"""
    return product_controller.get_all_products(db)


@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: str, db: Session = Depends(get_db)):
    """Get a single product by ID"""
    return product_controller.get_product_by_id(product_id, db)


@router.post("", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Create a new product (for admin/testing)"""
    return product_controller.create_product(product, db)
