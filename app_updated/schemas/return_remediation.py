from pydantic import BaseModel, Field
from datetime import date
 
# 🔹 Shared base schema
class ReturnRemediationBase(BaseModel):
    return_id: str = Field(..., alias="return_id")
    store_id: str = Field(..., alias="store_id")
    sku_id: str = Field(..., alias="sku_id")
    category: str = Field(..., alias="category")
    return_reason: str = Field(..., alias="return_reason")
    item_condition: str = Field(..., alias="item_condition")
    quantity_returned: int = Field(..., alias="quantity_returned")
    days_left: int = Field(..., alias="days_left")
    risk_level: str = Field(..., alias="risk_level")
    risk_score: float = Field(...,alias="risk_score")
    recommended_action: str = Field(..., alias="recommended_action")
    target_name: str = Field(..., alias="target_name")
    return_date: date = Field(..., alias="return_date")
    cost_price_cp: float = Field(..., alias="cost_price_cp")
    selling_price_sp: float = Field(..., alias="selling_price_sp")
    cogs: float = Field(..., alias="cogs")
    gross_margin: float = Field(..., alias="gross_margin")
    gross_margin_pct: float = Field(..., alias="gross_margin_pct")
    # expected_recovery: float = Field(..., alias="expected_recovery")
    # tax_benefit_amount: float = Field(..., alias="tax_benefit_amount")
    net_loss_mitigation: float = Field(..., alias="net_loss_mitigation")
    group_key: str = Field(..., alias="group_key")
    issue_id: str = Field(..., alias="issue_id")
 
    class Config:
        allow_population_by_field_name = True
        orm_mode = True
 
# 🔹 Schema for creation
class ReturnRemediationCreate(ReturnRemediationBase):
    pass
 
# 🔹 Schema for partial updates
class ReturnRemediationUpdate(BaseModel):
    return_id: str | None = None
    store_id: str | None = None
    sku_id: str | None = None
    category: str | None = None
    return_reason: str | None = None
    item_condition: str | None = None
    quantity_returned: int | None = None
    days_left: int | None = None
    risk_level: str | None = None
    risk_score: float | None = None
    recommended_action: str | None = None
    target_name: str | None = None
    return_date: date | None = None
    cost_price_cp: float | None = Field(None, alias="cost_price_cp")
    selling_price_sp: float | None = Field(None, alias="selling_price_sp")
    cogs: float | None = None
    gross_margin: float | None = None
    gross_margin_pct: float | None = None
    # expected_recovery: float | None = None
    # tax_benefit_amount: float | None = None
    net_loss_mitigation: float | None = None
    group_key: float | None = None
    issue_id: float | None = None
 
    class Config:
        allow_population_by_field_name = True
 
# 🔹 Schema for response
class ReturnRemediation(ReturnRemediationBase):
    id: int
 
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
 
 