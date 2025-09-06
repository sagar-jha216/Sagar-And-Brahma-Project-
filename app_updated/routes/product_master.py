# app/routes/product_master.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.product_master import ProductMaster, ProductMasterCreate
from app.database import get_db
from app.controllers.product_master import create_product, get_product_by_id

router = APIRouter()

@router.post("/", response_model=ProductMaster)
def create(product: ProductMasterCreate, db: Session = Depends(get_db)):
    return create_product(product, db)

@router.get("/{id}", response_model=ProductMaster)
def read(id: int, db: Session = Depends(get_db)):
    return get_product_by_id(id, db)
