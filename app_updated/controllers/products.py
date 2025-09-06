# app/controllers/products.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.products import Product as ProductModel
from app.schemas.products import ProductCreate

def create_product(product: ProductCreate, db: Session):
    db_product = ProductModel(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_all_products(db: Session):
    return db.query(ProductModel).all()

def get_product(id: str, db: Session):
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def delete_product(id: str, db: Session):
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return product



