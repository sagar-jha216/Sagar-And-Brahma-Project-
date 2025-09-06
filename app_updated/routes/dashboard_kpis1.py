from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.dashboard_kpis1 import get_dashboard_kpis1
from typing import Optional, List
from pydantic import BaseModel, Field
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# 📦 Filter model for incoming request
class FilterParams(BaseModel):
    Category: Optional[str] = Field(None, alias="Category")
    Sub_Category: Optional[str] = Field(None, alias="Sub_Category")
    Region_Historical: Optional[str] = Field(None, alias="Region_Historical")
    Store_ID: Optional[List[str]] = Field(None, alias="Store_ID")
    Store_Channel: Optional[List[str]] = Field(None, alias="Store_Channel")

    class Config:
        allow_population_by_field_name = True

# 🚀 Route to fetch formatted KPIs
@router.post("/kpis/formatted1", summary="Get formatted dashboard KPIs")
def get_kpi(filters: FilterParams, db: Session = Depends(get_db)):
    try:
        kpi_result = get_dashboard_kpis(filters, db)
        return {"status": "success", "data": kpi_result}
    except Exception as e:
        logger.error(f"Error fetching KPIs: {e}")
        raise HTTPException(status_code=500, detail="Failed to compute KPIs")
