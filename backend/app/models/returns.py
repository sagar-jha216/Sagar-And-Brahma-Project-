from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

class Return(Base):
    __tablename__ = "returns"
    id = Column(Integer, primary_key=True, index=True)
    return_id = Column(String, index=True)
    store_id = Column(String)
    sku_id = Column(String)
    category = Column(String)
    product_name = Column(String)
    return_reason = Column(String)
    item_condition = Column(String)
    quantity_returned = Column(Integer)
    cost_price = Column(Float)
    selling_price = Column(Float)
    shelf_life = Column(Integer)
    days_left = Column(Integer)
    return_date = Column(Date)
    customer_id = Column(String)
    original_purchase_date = Column(Date)
    created_at = Column(Date)
    updated_at = Column(Date)