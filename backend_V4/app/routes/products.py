# app/routes/products.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.products import Product, ProductCreate
from app.database import get_db
from app.controllers.products import create_product, get_product, delete_product, get_all_products
from typing import List

router = APIRouter()
@router.post("/", response_model=Product)
def create(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(product, db)

@router.get("/", response_model=List[Product])
def get_all(db: Session = Depends(get_db)):
    return get_all_products(db)

@router.get("/{id}", response_model=Product)
def read(id: str, db: Session = Depends(get_db)):
    return get_product(id, db)

@router.delete("/{id}", response_model=Product)
def delete(id: str, db: Session = Depends(get_db)):
    return delete_product(id, db)
 
