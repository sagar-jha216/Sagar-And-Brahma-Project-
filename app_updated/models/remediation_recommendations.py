from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
 
class RemediationRecommendation(Base):
    __tablename__ = "remediation_recommendations"
 
    id = Column(Integer, primary_key=True, index=True)
 
    sku_id = Column(String, ForeignKey("inventory.SKU_ID"), nullable=False, name="sku_id")
    inventory_item = relationship("Inventory", back_populates="recommendations")
 
    product_name = Column(String, name="product_name")
    category = Column(String, name="category")
 
    store_id = Column(String, ForeignKey("stores.Store_ID"), nullable=False, name="store_id")
    store = relationship("Store", back_populates="recommendations")
 
    
    received_date = Column(Date, name="received_date")
    quantity_on_hand = Column(Integer, name="quantity_on_hand")
    sell_through_rate = Column(Float, name="sell_through_rate")
    Sell_Through_Rate_Per_Day = Column(Float, name="Sell_Through_Rate_Per_Day")
    shelf_life_remaining = Column(Integer, name="shelf_life_remaining")
    inventory_age_days = Column(Integer, name="inventory_age_days")
    shrinkage_risk = Column(String, name="shrinkage_risk")
    risk_level = Column(String, name="risk_level")
    recommended_action = Column(String, name="recommended_action")
    target_name = Column(String, name="target_name")
    action_quantity = Column(Float, name="action_quantity")
    unit_cost = Column(Float, name="unit_cost")
    unit_price = Column(Float, name="unit_price")
    # original_revenue = Column(Float, name="original_revenue")   #as per new databse this column has been removed
    cogs = Column(Float, name="cogs")
    gross_margin = Column(Float, name="gross_margin")
    gross_margin_pct = Column(Float, name="gross_margin_pct")
    # expected_recovery = Column(Float, name="expected_recovery")  #as per new databse this column has been removed
    transport_cost = Column(Float, name="transport_cost")
    net_loss_mitigation = Column(Float, name="net_loss_mitigation")
    # tax_benefit_amount = Column(Float, name="tax_benefit_amount") 
    upliftment = Column(Float, name="upliftment")
    recommendation_rank = Column(Integer, name="recommendation_rank")
    group_key = Column(String, name="group_key")
    issue_id = Column(String, name="issue_id")
 
 