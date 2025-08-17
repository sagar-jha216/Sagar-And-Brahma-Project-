"""
Partner models for ShrinkSense (NGO and Liquidation partners)
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Text
from datetime import datetime

from .base import Base

class NGOPartner(Base):
    __tablename__ = "ngo_partners"
    
    ngo_id = Column(String, primary_key=True)
    ngo_name = Column(String, nullable=False)
    contact_person = Column(String)
    phone_number = Column(String)
    email = Column(String)
    address = Column(Text)
    city = Column(String)
    state = Column(String)
    capacity_limit = Column(Integer)
    current_capacity = Column(Integer)
    partnership_start_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class LiquidationPartner(Base):
    __tablename__ = "liquidation_partners"
    
    partner_id = Column(String, primary_key=True)
    partner_name = Column(String, nullable=False)
    contact_person = Column(String)
    phone_number = Column(String)
    email = Column(String)
    address = Column(Text)
    city = Column(String)
    state = Column(String)
    rate_per_kg = Column(Float)
    capacity_limit = Column(Integer)
    current_capacity = Column(Integer)
    partnership_start_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)