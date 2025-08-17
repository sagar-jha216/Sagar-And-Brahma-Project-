"""
Product master model for ShrinkSense
"""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base

class ProductMaster(Base):
    __tablename__ = "product_master"
    
    sku_id = Column(String, primary_key=True)
    product_name = Column(String, nullable=False)
    brand = Column(String)
    brand_code = Column(String)
    category = Column(String, nullable=False)
    sub_category = Column(String)
    pack_size = Column(String)
    unit_of_measure = Column(String)
    storage_type = Column(String)
    supplier_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    inventory_items = relationship("Inventory", back_populates="product")
    return_items = relationship("Returns", back_populates="product")