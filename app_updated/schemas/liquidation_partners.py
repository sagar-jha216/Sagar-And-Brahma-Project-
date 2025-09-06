from pydantic import BaseModel, Field
from typing import Optional

# 🔹 Base schema shared by Create, Read, and Update
class LiquidatorBase(BaseModel):
    Liquidator_ID: str = Field(..., alias="Liquidator_ID")
    Liquidator_Name: str = Field(..., alias="Liquidator_Name")
    Liquidator_Type: str = Field(..., alias="Liquidator_Type")
    Latitude: float = Field(..., alias="Latitude")
    Longitude: float = Field(..., alias="Longitude")
    Offer_Price_Pct_of_MRP: float = Field(..., alias="Offer_Price_Pct_of_MRP")
    Pickup_SLA_Days: int = Field(..., alias="Pickup_SLA_Days")
    Quantity_Handling_Capacity_Fresh_Produce: int = Field(..., alias="Quantity_Handling_Capacity_Fresh_Produce")
    Quantity_Handling_Capacity_Dry_Goods: int = Field(..., alias="Quantity_Handling_Capacity_Dry_Goods")
    Quantity_Handling_Capacity_GM: int = Field(..., alias="Quantity_Handling_Capacity_GM")
    Past_Fulfillment_Success_Rate_Pct: float = Field(..., alias="Past_Fulfillment_Success_Rate_Pct")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True  # Enables compatibility with SQLAlchemy models

# 🔹 For POST requests
class LiquidatorCreate(LiquidatorBase):
    pass

# 🔹 For PATCH/PUT requests (partial updates)
class LiquidatorUpdate(BaseModel):
    Liquidator_ID: Optional[str] = Field(None, alias="Liquidator_ID")
    Liquidator_Name: Optional[str] = Field(None, alias="Liquidator_Name")
    Liquidator_Type: Optional[str] = Field(None, alias="Liquidator_Type")
    Latitude: Optional[float] = Field(None, alias="Latitude")
    Longitude: Optional[float] = Field(None, alias="Longitude")
    Offer_Price_Pct_of_MRP: Optional[float] = Field(None, alias="Offer_Price_Pct_of_MRP")
    Pickup_SLA_Days: Optional[int] = Field(None, alias="Pickup_SLA_Days")
    Quantity_Handling_Capacity_Fresh_Produce: Optional[int] = Field(None, alias="Quantity_Handling_Capacity_Fresh_Produce")
    Quantity_Handling_Capacity_Dry_Goods: Optional[int] = Field(None, alias="Quantity_Handling_Capacity_Dry_Goods")
    Quantity_Handling_Capacity_GM: Optional[int] = Field(None, alias="Quantity_Handling_Capacity_GM")
    Past_Fulfillment_Success_Rate_Pct: Optional[float] = Field(None, alias="Past_Fulfillment_Success_Rate_Pct")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True

# 🔹 For GET responses
class LiquidationPartner(LiquidatorBase):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
