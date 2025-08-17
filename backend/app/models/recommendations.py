"""
Recommendation models for ShrinkSense
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from datetime import datetime

from .base import Base

class RemediationRecommendation(Base):
    __tablename__ = "remediation_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    sku_id = Column(String, nullable=False)
    store_id = Column(String, nullable=False)
    recommendation_type = Column(String, nullable=True)
    priority = Column(String, default="medium")
    estimated_value = Column(Float)
    potential_savings = Column(Float)
    reason = Column(Text)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class ReturnRemediation(Base):
    __tablename__ = "return_remediation"
    
    id = Column(Integer, primary_key=True, index=True)
    return_id = Column(Integer, ForeignKey("returns.id"), nullable=False)
    recommended_action = Column(String, nullable=True)
    estimated_recovery = Column(Float)
    partner_id = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)