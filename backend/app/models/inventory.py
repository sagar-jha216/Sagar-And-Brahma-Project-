"""
Inventory model for ShrinkSense with extended Excel columns
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base

class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    sku_id = Column(String, ForeignKey("product_master.sku_id"), nullable=False)
    store_id = Column(String, ForeignKey("stores.store_id"), nullable=False)
    
    # Basic inventory data
    current_stock = Column(Integer, default=0)
    min_stock_level = Column(Integer, default=0)
    max_stock_level = Column(Integer, default=0)
    reorder_point = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)
    cost_price = Column(Float)
    selling_price = Column(Float)
    
    # Excel data columns for shrinkage calculation
    system_quantity_received = Column(Integer, default=0)
    actual_quantity_received = Column(Integer, default=0)
    number_damaged_units = Column(Integer, default=0)
    number_dump_units = Column(Integer, default=0)
    number_expired_units = Column(Integer, default=0)
    inventory_on_hand = Column(Integer, default=0)
    unit_sold = Column(Integer, default=0)
    days_active = Column(Integer, default=0)
    shelf_life = Column(Integer, default=0)
    sell_through_rate_per_day = Column(Float, default=0.0)
    sell_through_rate = Column(Float, default=0.0)
    shelf_life_remaining = Column(Integer, default=0)
    shelf_life_used_pct = Column(Float, default=0.0)
    projected_sales_remaining = Column(Float, default=0.0)
    inventory_status = Column(String)
    original_revenue = Column(Float, default=0.0)
    cogs = Column(Float, default=0.0)
    original_gross_margin = Column(Float, default=0.0)
    inventory_age_days = Column(Integer, default=0)
    is_returnable = Column(Boolean, default=False)
    is_perishable = Column(Boolean, default=False)
    region = Column(Integer, default=0)
    historical_markdown_pct = Column(Float, default=0.0)
    days_of_supply = Column(Float, default=0.0)
    required_markdown_pct = Column(Float, default=0.0)
    predicted_upliftment_factor = Column(Float, default=0.0)
    
    # Calculated shrinkage percentage
    shrinkage_percentage = Column(Float, default=0.0)
    
    # Relationships
    product = relationship("ProductMaster", back_populates="inventory_items")
    store = relationship("Store", back_populates="inventory_items")