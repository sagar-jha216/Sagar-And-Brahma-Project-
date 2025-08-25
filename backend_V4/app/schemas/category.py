# app/schemas/Category.py
from pydantic import BaseModel

class CategoryBase(BaseModel):
    category_name: str


class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True
