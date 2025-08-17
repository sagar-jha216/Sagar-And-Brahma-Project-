"""
Returns model for ShrinkSense
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base

class Returns(Base):
    __tablename__ = "returns"
    
    id = Column(Integer, primary_key=True, index=True)
    sku_id = Column(String, ForeignKey("product_master.sku_id"), nullable=False)
    store_id = Column(String, ForeignKey("stores.store_id"), nullable=False)
    return_date = Column(DateTime, default=datetime.utcnow)
    quantity_returned = Column(Integer, nullable=False)
    reason = Column(String)
    condition = Column(String)
    value = Column(Float)
    status = Column(String, default="pending")  # pending, processed, disposed
    
    # Relationships
    product = relationship("ProductMaster", back_populates="return_items")
    store = relationship("Store", back_populates="return_items")