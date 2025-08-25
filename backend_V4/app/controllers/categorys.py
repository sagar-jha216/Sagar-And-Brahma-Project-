from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.category import Category as CategoryModel
from app.schemas.category import CategoryCreate

def create_category(category: CategoryCreate, db: Session):
    db_category = CategoryModel(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_all_categories(db: Session):
    return db.query(CategoryModel).all()


def get_category(id: int, db: Session):
    category = db.query(CategoryModel).filter(CategoryModel.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

def delete_category(id: int, db: Session):
    category = db.query(CategoryModel).filter(CategoryModel.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return category
