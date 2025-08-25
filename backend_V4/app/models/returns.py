from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Return(Base):
    __tablename__ = "returns"

    return_id = Column("return_id", String, primary_key=True, index=True)
    store_id = Column("store_id", String, ForeignKey("stores.Store_ID"), nullable=False)
    store = relationship("Store", back_populates="returns")

    sku_id = Column("sku_id", String, ForeignKey("inventory.SKU_ID"), nullable=False)
    inventory_item = relationship("Inventory", back_populates="returns")

    category = Column("category", String)
    product_name = Column("product_name", String)
    return_reason = Column("return_reason", String)
    quantity_returned = Column("quantity_returned", Integer)
    Cost_Price_CP = Column("Cost_Price_CP", Float)
    Selling_Price_SP = Column("Selling_Price_SP", Float)
    shelf_life = Column("shelf_life", Integer)
    days_left = Column("days_left", Integer)
    return_date = Column("return_date", DateTime)
    customer_id = Column("customer_id", String)
    original_purchase_date = Column("original_purchase_date", DateTime)
    created_at = Column("created_at", DateTime)
    updated_at = Column("updated_at", DateTime)
