from sqlalchemy import Column, String, Float, Integer
from app.database import Base

class RetailKPI(Base):
    __tablename__ = "retail_kpi"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    inventory_accuracy = Column(Float)
    damage_percent = Column(Float)
    dump_percent = Column(Float)
    expired_percent = Column(Float)
    aged_percent = Column(Float)
    return_percent = Column(Float)

