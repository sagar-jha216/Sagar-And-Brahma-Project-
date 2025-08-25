from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    SKU_ID = Column(String, primary_key=True, index=True)
    Product_Name = Column(String)
    Category = Column(String)
    Store_ID = Column(String, ForeignKey("stores.Store_ID"), nullable=False)

    store = relationship("Store", back_populates="inventory_items")

    Supplier_Name = Column(String)
    Received_Date = Column(DateTime)
    Expiry_Date = Column(DateTime)
    System_Quantity_Received = Column(Integer)
    Actual_Quantity_Received = Column(Integer)
    Difference_System_Actual = Column(Integer)  
    Number_Damaged_Units = Column(Integer)
    Number_Dump_Units = Column(Integer)
    Number_Expired_Units = Column(Integer)
    Inventory_On_Hand = Column(Integer)
    Unit_Sold = Column(Integer)
    Days_Active = Column(Integer)
    Shelf_Life = Column(Integer)
    Sell_Through_Rate_Per_Day = Column(Float)
    Sell_Through_Rate = Column(Float)
    Shelf_Life_Remaining = Column(Integer)
    Shelf_Life_Used_Pct = Column(Float)
    Inventory_Status = Column(String)
    Cost_Price_CP = Column(Float)
    Selling_Price_SP = Column(Float)
    Original_Revenue_no_return_remediation = Column(Float)
    COGS = Column(Float)
    Original_Gross_Margin = Column(Float)
    Inventory_Age_Days = Column(Integer)
    Is_Returnable = Column(Boolean)
    Is_Perishable = Column(Boolean)
    Region_Historical = Column(String)
    Markdown_Pct = Column(Float)
    Days_of_Supply = Column(Integer)
    Required_Markdown_Pct = Column(Float)
    Predicted_Upliftment_Factor = Column(Float)
    Sub_Category = Column(String)
    Store_Channel = Column(String)


    returns = relationship("Return", back_populates="inventory_item")
    remediations = relationship("ReturnRemediation", back_populates="inventory_item")
    recommendations = relationship("RemediationRecommendation", back_populates="inventory_item")
