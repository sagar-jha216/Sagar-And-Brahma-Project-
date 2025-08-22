from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ReturnRemediation(Base):
    __tablename__ = "return_remediation"

    id = Column(Integer, primary_key=True, index=True)
    return_id = Column(String, index=True, name="return_id")

    store_id = Column(String, ForeignKey("stores.Store_ID"), nullable=False, name="store_id")
    store = relationship("Store", back_populates="return_remediations")

    sku_id = Column(String, ForeignKey("inventory.SKU_ID"), nullable=False, name="sku_id")
    inventory_item = relationship("Inventory", back_populates="remediations")

    category = Column(String, name="category")
    return_reason = Column(String, name="return_reason")
    item_condition = Column(String, name="item_condition")
    quantity_returned = Column(Integer, name="quantity_returned")
    days_left = Column(Integer, name="days_left")
    risk_level = Column(String, name="risk_level")
    recommended_action = Column(String, name="recommended_action")
    target_name = Column(String, name="target_name")
    return_date = Column(Date, name="return_date")
    cost_price_cp = Column(Float, name="cost_price(cp)")
    selling_price_sp = Column(Float, name="selling_price(sp)")
    gross_margin_pct = Column(Float, name="gross_margin_pct")
    expected_recovery = Column(Float, name="expected_recovery")
    tax_benefit_amount = Column(Float, name="tax_benefit_amount")
    net_loss_mitigation = Column(Float, name="net_loss_mitigation")
