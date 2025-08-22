from pydantic import BaseModel, Field

class StoreBase(BaseModel):
    Store_ID: str = Field(..., alias="Store_ID")
    Store_Name: str = Field(..., alias="Store_Name")
    Store_City: str = Field(..., alias="Store_City")
    Store_State: str = Field(..., alias="Store_State")
    Store_Region: str = Field(..., alias="Store_Region")
    Latitude: float = Field(..., alias="Latitude")
    Longitude: float = Field(..., alias="Longitude")
    Capacity_Limit: int = Field(..., alias="Capacity_Limit")
    Current_Capacity: int = Field(..., alias="Current_Capacity")
    Performance_Score: float = Field(..., alias="Performance_Score")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True

class StoreCreate(StoreBase):
    pass

class Store(StoreBase):
    id: int
