"""
Store model for ShrinkSense
"""

from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base

class Store(Base):
    __tablename__ = "stores"
    
    store_id = Column(String, primary_key=True)
    store_name = Column(String, nullable=False)
    store_city = Column(String)
    store_state = Column(String)
    store_region = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    capacity_limit = Column(Integer)
    current_capacity = Column(Integer)
    performance_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    inventory_items = relationship("Inventory", back_populates="store")
    return_items = relationship("Returns", back_populates="store")