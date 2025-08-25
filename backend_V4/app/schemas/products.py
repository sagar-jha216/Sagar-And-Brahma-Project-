# app/schemas/products.py
from pydantic import BaseModel

class ProductBase(BaseModel):
    product_name: str
    category_id: int


class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id:int
    class Config:
        from_attributes = True
