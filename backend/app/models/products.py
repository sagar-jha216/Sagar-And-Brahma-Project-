# app/models/products.py
from sqlalchemy import Column, String
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    sku_id = Column(String, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    category_id = Column(String, nullable=False)

