from pydantic import BaseModel, Field

class ProductMasterBase(BaseModel):
    SKU_ID: str = Field(..., alias="SKU_ID")
    Product_Name: str = Field(..., alias="Product_Name")
    Brand: str = Field(..., alias="Brand")
    Brand_Code: str = Field(..., alias="Brand Code")
    Category: str = Field(..., alias="Category")
    Sub_Category: str = Field(..., alias="Sub_Category")
    Pack_Size: str = Field(..., alias="Pack_Size")
    Unit_Of_Measure: str = Field(..., alias="Unit_Of_Measure")
    Storage_Type: str = Field(..., alias="Storage_Type")
    Supplier_Name: str = Field(..., alias="Supplier_Name")

    class Config:
        allow_population_by_field_name = True

class ProductMasterCreate(ProductMasterBase):
    pass

class ProductMaster(ProductMasterBase):
    id: int

    class Config:
        from_attributes = True
        allow_population_by_field_name = True
