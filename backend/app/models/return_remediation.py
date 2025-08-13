from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

class ReturnRemediation(Base):
    __tablename__ = "return_remediation"
    id = Column(Integer, primary_key=True, index=True)
    return_id = Column(String, index=True)
    store_id = Column(String)
    sku_id = Column(String)
    category = Column(String)
    return_reason = Column(String)
    item_condition = Column(String)
    quantity_returned = Column(Integer)
    days_left = Column(Integer)
    risk_level = Column(String)
    recommended_action = Column(String)
    target_name = Column(String)
    return_date = Column(Date)
    cost_price = Column(Float)
    selling_price = Column(Float)
    gross_margin_pct = Column(Float)
    expected_recovery = Column(Float)
    tax_benefit_amount = Column(Float)
    net_loss_mitigation = Column(Float)