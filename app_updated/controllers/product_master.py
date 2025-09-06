# app/controllers/product_master.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.product_master import ProductMaster as ProductMasterModel
from app.schemas.product_master import ProductMasterCreate

def create_product(product: ProductMasterCreate, db: Session):
    db_product = ProductMasterModel(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product_by_id(product_id: int, db: Session):
    product = db.query(ProductMasterModel).filter(ProductMasterModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product record not found")
    return product

def get_product_by_sku(sku_id: str, db: Session):
    product = db.query(ProductMasterModel).filter(ProductMasterModel.SKU_ID == sku_id).all()
    if not product:
        raise HTTPException(status_code=404, detail="No product found for this SKU")
    return product

def update_product(product_id: int, product_update: ProductMasterCreate, db: Session):
    product = db.query(ProductMasterModel).filter(ProductMasterModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product record not found")
    
    for key, value in product_update.dict(exclude_unset=True).items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product

def delete_product(product_id: int, db: Session):
    product = db.query(ProductMasterModel).filter(ProductMasterModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product record not found")
    
    db.delete(product)
    db.commit()
    return {"detail": "Product record deleted successfully"}
