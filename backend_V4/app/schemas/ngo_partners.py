from pydantic import BaseModel, Field

class NGOPartnerBase(BaseModel):
    NGO_ID: str = Field(..., alias="NGO_ID")
    NGO_Name: str = Field(..., alias="NGO_Name")
    NGO_Type: str = Field(..., alias="NGO_Type")
    NGO_LAT: float = Field(..., alias="NGO_LAT")
    NGO_LONG: float = Field(..., alias="NGO_LONG")
    Acceptance_Criteria_Met: bool = Field(..., alias="Acceptance_Criteria_Met")
    Acceptance_Capacity_Fresh_Produce: int = Field(..., alias="Acceptance_Capacity_Fresh_Produce")
    Acceptance_Capacity_Dry_Goods: int = Field(..., alias="Acceptance_Capacity_Dry_Goods")
    Acceptance_Capacity_GM: int = Field(..., alias="Acceptance_Capacity_GM")
    Past_Donation_Success_Rate: float = Field(..., alias="Past_Donation_Success_Rate")

    class Config:
        allow_population_by_field_name = True  # Enables using Pythonic names in code

class NGOPartnerCreate(NGOPartnerBase):
    pass

class NGOPartner(NGOPartnerBase):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
