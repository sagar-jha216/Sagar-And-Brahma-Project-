from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(String, unique=False, index=True)
    store_name = Column(String)
    store_city = Column(String)
    store_state = Column(String)
    store_region = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    capacity_limit = Column(Integer)
    current_capacity = Column(Integer)
    performance_score = Column(Float)

app/models/ngo_partners.py


python
CopyEdit
from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class NGOPartner(Base):
    __tablename__ = "ngo_partners"
    id = Column(Integer, primary_key=True, index=True)
    ngo_id = Column(String, index=True)
    ngo_name = Column(String)
    ngo_type = Column(String)
    ngo_lat = Column(Float)
    ngo_long = Column(Float)
    acceptance_criteria_met = Column(Boolean)
    acceptance_capacity_fresh_produce = Column(Integer)
    acceptance_capacity_dry_goods = Column(Integer)
    acceptance_capacity_gm = Column(Integer)
    past_donation_success_rate = Column(Float)