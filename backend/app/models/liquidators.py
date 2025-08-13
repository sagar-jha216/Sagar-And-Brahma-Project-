from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Liquidator(Base):
    __tablename__ = "liquidators"
    id = Column(Integer, primary_key=True, index=True)
    liquidator_id = Column(String, index=True)
    liquidator_name = Column(String)
    liquidator_type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    offer_price_pct_of_mrp = Column(Float)
    pickup_sla_days = Column(Integer)
    quantity_handling_capacity_fresh_produce = Column(Integer)
    quantity_handling_capacity_dry_goods = Column(Integer)
    quantity_handling_capacity_gm = Column(Integer)
    past_fulfillment_success_rate_pct = Column(Float)
