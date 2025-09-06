# app/routes/category.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.category import CategoryCreate, Category
from app.database import get_db
from app.controllers.categorys import create_category, get_category, get_all_categories, delete_category
from typing import List

router = APIRouter()
@router.post("/", response_model=Category)
def create(category: CategoryCreate, db: Session = Depends(get_db)):
    print(category,"1")
    return create_category(category, db)

@router.get("/", response_model=List[Category])
def get_all(db: Session = Depends(get_db)):
    return get_all_categories(db)

@router.get("/{id}", response_model=Category)
def read(id: str, db: Session = Depends(get_db)):
    return get_category(id, db)

@router.delete("/{id}", response_model=Category)
def delete(id: str, db: Session = Depends(get_db)):
    return delete_category(id, db)
 
