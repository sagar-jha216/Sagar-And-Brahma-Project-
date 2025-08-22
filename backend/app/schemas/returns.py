from pydantic import BaseModel, Field
from datetime import date

# 🔹 Shared base schema
class ReturnBase(BaseModel):
    return_id: str = Field(..., alias="return_id")
    store_id: str = Field(..., alias="store_id")
    sku_id: str = Field(..., alias="sku_id")
    category: str = Field(..., alias="category")
    product_name: str = Field(..., alias="product_name")
    return_reason: str = Field(..., alias="return_reason")
    quantity_returned: int = Field(..., alias="quantity_returned")
    Cost_Price_CP: float = Field(..., alias="Cost_Price(CP)")
    Selling_Price_SP: float = Field(..., alias="Selling_Price(SP)")
    shelf_life: int = Field(..., alias="shelf_life")
    days_left: int = Field(..., alias="days_left")
    return_date: date = Field(..., alias="return_date")
    customer_id: str = Field(..., alias="customer_id")
    original_purchase_date: date = Field(..., alias="original_purchase_date")
    created_at: date = Field(..., alias="created_at")
    updated_at: date = Field(..., alias="updated_at")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True

# 🔹 Schema for creating a new return record
class ReturnCreate(ReturnBase):
    pass

# 🔹 Schema for partial updates
class ReturnUpdate(BaseModel):
    return_id: str | None = None
    store_id: str | None = None
    sku_id: str | None = None
    category: str | None = None
    product_name: str | None = None
    return_reason: str | None = None
    quantity_returned: int | None = None
    Cost_Price_CP: float | None = Field(None, alias="Cost_Price(CP)")
    Selling_Price_SP: float | None = Field(None, alias="Selling_Price(SP)")
    shelf_life: int | None = None
    days_left: int | None = None
    return_date: date | None = None
    customer_id: str | None = None
    original_purchase_date: date | None = None
    created_at: date | None = None
    updated_at: date | None = None

    class Config:
        allow_population_by_field_name = True

# 🔹 Schema for returning data (includes ID)
class Return(ReturnBase):
    id: int
