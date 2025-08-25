from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class NGOPartner(Base):
    __tablename__ = "ngo_partners"

    id = Column(Integer, primary_key=True, index=True)
    NGO_ID = Column(String, index=True, name="NGO_ID")
    NGO_Name = Column(String, name="NGO_Name")
    NGO_Type = Column(String, name="NGO_Type")
    NGO_LAT = Column(Float, name="NGO_LAT")
    NGO_LONG = Column(Float, name="NGO_LONG")
    Acceptance_Criteria_Met = Column(Boolean, name="Acceptance_Criteria_Met")
    Acceptance_Capacity_Fresh_Produce = Column(Integer, name="Acceptance_Capacity_Fresh_Produce")
    Acceptance_Capacity_Dry_Goods = Column(Integer, name="Acceptance_Capacity_Dry_Goods")
    Acceptance_Capacity_GM = Column(Integer, name="Acceptance_Capacity_GM")
    Past_Donation_Success_Rate = Column(Float, name="Past_Donation_Success_Rate")
