from pydantic import BaseModel, Field
from datetime import date

class InventoryBase(BaseModel):
    SKU_ID: str = Field(..., alias="SKU_ID")
    Product_Name: str = Field(..., alias="Product_Name")
    Category: str = Field(..., alias="Category")
    Sub_Category: str = Field(..., alias="Sub_Category")
    Store_ID: str = Field(..., alias="Store_ID")
    Store_Channel: str = Field(..., alias="Store_Channel")
    Supplier_Name: str = Field(..., alias="Supplier_Name")
    Received_Date: date = Field(..., alias="Received_Date")
    Expiry_Date: date = Field(..., alias="Expiry_Date")
    System_Quantity_Received: int = Field(..., alias="System_Quantity_Received")
    Actual_Quantity_Received: int = Field(..., alias="Actual_Quantity_Received")
    Difference_System_Actual: int = Field(..., alias="Difference_(System - Actual)")
    Number_Damaged_Units: int = Field(..., alias="Number_Damaged_Units")
    Number_Dump_Units: int = Field(..., alias="Number_Dump_Units")
    Number_Expired_Units: int = Field(..., alias="Number_Expired_Units")
    Inventory_On_Hand: int = Field(..., alias="Inventory_On_Hand")
    Unit_Sold: int = Field(..., alias="Unit_Sold")
    Days_Active: int = Field(..., alias="Days_Active")
    Shelf_Life: int = Field(..., alias="Shelf_Life")
    Sell_Through_Rate_Per_Day: float = Field(..., alias="Sell_Through_Rate_Per_Day")
    Sell_Through_Rate: float = Field(..., alias="Sell_Through_Rate")
    Shelf_Life_Remaining: int = Field(..., alias="Shelf_Life_Remaining")
    Shelf_Life_Used_Pct: float = Field(..., alias="Shelf_Life_Used_Pct")
    Projected_Sales_Remaining: float = Field(..., alias="Projected_Sales_Remaining")
    Inventory_Status: str = Field(..., alias="Inventory_Status")
    Cost_Price_CP: float = Field(..., alias="Cost_Price_CP")
    Selling_Price_SP: float = Field(..., alias="Selling_Price_SP")
    Original_Revenue: float = Field(..., alias="Original_Revenue")
    COGS: float = Field(..., alias="COGS")
    Original_Gross_Margin: float = Field(..., alias="Original_Gross_Margin")
    Inventory_Age_Days: int = Field(..., alias="Inventory_Age_Days")
    Is_Returnable: bool = Field(..., alias="Is_Returnable")
    Is_Perishable: bool = Field(..., alias="Is_Perishable")
    Region_Historical: str = Field(..., alias="Region_Historical")
    Markdown_Pct: float = Field(..., alias="Markdown_Pct")
    Days_of_Supply: int = Field(..., alias="Days of Supply")
    Required_Markdown_Pct: float = Field(..., alias="Required_Markdown_Pct")
    Predicted_Upliftment_Factor: float = Field(..., alias="Predicted_Upliftment_Factor")
    
    


    class Config:
        allow_population_by_field_name = True  # Allows using Pythonic names in code

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int

    class Config:
        from_attributes = True
        allow_population_by_field_name = True
