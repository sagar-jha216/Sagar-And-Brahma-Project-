from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class LiquidationPartner(Base):
    __tablename__ = "liquidation_partners"

    id = Column(Integer, primary_key=True, index=True)
    Liquidator_ID = Column(String, index=True, name="Liquidator_ID")
    Liquidator_Name = Column(String, name="Liquidator_Name")
    Liquidator_Type = Column(String, name="Liquidator_Type")
    Latitude = Column(Float, name="Latitude")
    Longitude = Column(Float, name="Longitude")
    Offer_Price_Pct_of_MRP = Column(Float, name="Offer Price (% of MRP)")
    Pickup_SLA_Days = Column(Integer, name="Pickup SLA (in days)")
    Quantity_Handling_Capacity_Fresh_Produce = Column(Integer, name="Quantity_Handling_Capacity_Fresh_Produce")
    Quantity_Handling_Capacity_Dry_Goods = Column(Integer, name="Quantity_Handling_Capacity_Dry_Goods")
    Quantity_Handling_Capacity_GM = Column(Integer, name="Quantity_Handling_Capacity_GM")
    Past_Fulfillment_Success_Rate_Pct = Column(Float, name="Past Fulfillment Success Rate (%)")

