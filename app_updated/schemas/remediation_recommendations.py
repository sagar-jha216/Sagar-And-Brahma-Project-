from pydantic import BaseModel, Field
from datetime import date
 
# 🔹 Shared base schema
class RemediationRecommendationBase(BaseModel):
    sku_id: str = Field(..., alias="sku_id")
    product_name: str = Field(..., alias="product_name")
    category: str = Field(..., alias="category")
    store_id: str = Field(..., alias="store_id")
    received_date: date = Field(..., alias="received_date")
    quantity_on_hand: int = Field(..., alias="quantity_on_hand")
    sell_through_rate: float = Field(..., alias="sell_through_rate")
    Sell_Through_Rate_Per_Day: float = Field(..., alias="Sell_Through_Rate_Per_Day")
    shelf_life_remaining: int = Field(..., alias="shelf_life_remaining")
    inventory_age_days: int = Field(..., alias="inventory_age_days")
    shrinkage_risk: str = Field(..., alias="shrinkage_risk")
    risk_level: str = Field(..., alias="risk_level")
    recommended_action: str = Field(..., alias="recommended_action")
    target_name: str = Field(..., alias="target_name")
    action_quantity: float = Field(..., alias="action_quantity")
    unit_cost: float = Field(..., alias="unit_cost")
    unit_price: float = Field(..., alias="unit_price")
    # original_revenue: float = Field(..., alias="original_revenue") #this column has been removed from new database
    cogs: float = Field(..., alias="cogs")
    gross_margin: float = Field(..., alias="gross_margin")
    gross_margin_pct: float = Field(..., alias="gross_margin_pct")
    # expected_recovery: float = Field(..., alias="expected_recovery") #this column has been removed from new database
    transport_cost: float = Field(..., alias="transport_cost")
    net_loss_mitigation: float = Field(..., alias="net_loss_mitigation")
    # tax_benefit_amount: float = Field(..., alias="tax_benefit_amount")  #this column has been removed from new database
    upliftment: float = Field(..., alias="upliftment")
    recommendation_rank: int = Field(..., alias="recommendation_rank")
    group_key: str = Field(..., alias="group_key")
    issue_id: str = Field(..., alias="issue_id")
 
    class Config:
        allow_population_by_field_name = True
        orm_mode = True  # Ensures compatibility with SQLAlchemy models
 
# 🔹 Schema for creation
class RemediationRecommendationCreate(RemediationRecommendationBase):
    pass
 
# 🔹 Schema for update (partial updates allowed)
class RemediationRecommendationUpdate(BaseModel):
    sku_id: str | None = None
    product_name: str | None = None
    category: str | None = None
    store_id: str | None = None
    received_date: date | None = None
    quantity_on_hand: int | None = None
    sell_through_rate: float | None = None
    Sell_Through_Rate_Per_Day: float | None = None
    shelf_life_remaining: int | None = None
    inventory_age_days: int | None = None
    shrinkage_risk: str | None = None
    risk_level: str | None = None
    recommended_action: str | None = None
    target_name: str | None = None
    action_quantity: float | None = None
    unit_cost: float | None = None
    unit_price: float | None = None
    # original_revenue: float | None = None
    cogs: float | None = None
    gross_margin: float | None = None
    gross_margin_pct: float | None = None
    # expected_recovery: float | None = None
    transport_cost: float | None = None
    net_loss_mitigation: float | None = None
    # tax_benefit_amount: float | None = None
    recommendation_rank: int | None = None
    group_key: str | None = None
    issue_id: str | None = None
 
    class Config:
        allow_population_by_field_name = True
 
# 🔹 Schema for response
class RemediationRecommendation(RemediationRecommendationBase):
    id: int
 
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
 
 