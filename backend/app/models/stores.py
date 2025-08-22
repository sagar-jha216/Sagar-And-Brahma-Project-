from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Store(Base):
    __tablename__ = "stores"

    Store_ID = Column("Store_ID", String, primary_key=True, index=True)
    Store_Name = Column("Store_Name", String)
    Store_City = Column("Store_City", String)
    Store_State = Column("Store_State", String)
    Store_Region = Column("Store_Region", String)
    Latitude = Column("Latitude", Float)
    Longitude = Column("Longitude", Float)
    Capacity_Limit = Column("Capacity_Limit", Integer)
    Current_Capacity = Column("Current_Capacity", Integer)
    Performance_Score = Column("Performance_Score", Float)

    inventory_items = relationship("Inventory", back_populates="store")
    returns = relationship("Return", back_populates="store")
    return_remediations = relationship("ReturnRemediation", back_populates="store")
    recommendations = relationship("RemediationRecommendation", back_populates="store")
