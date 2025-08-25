
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.dashboard_graphs import get_dashboard
from typing import Optional, List
from datetime import date
import logging
from pydantic import BaseModel,Field

router = APIRouter()
logger = logging.getLogger(__name__)




class FilterParams(BaseModel):
    Category: Optional[str] = Field(None, alias="Category")
    Sub_Category: Optional[str] = Field(None, alias="Sub_Category")
    Region_Historical: Optional[str] = Field(None, alias="Region_Historical")
    Store_ID: Optional[List[str]] = Field(None, alias="Store_ID")
    Store_Channel: Optional[List[str]] = Field(None, alias="Store_Channel")

    class Config:
        allow_population_by_field_name = True

@router.post("/dashboard")
def get_kpi(filters: FilterParams, db:Session = Depends(get_db)):
    kpi_result = get_dashboard(filters,db)
    return kpi_result
  









