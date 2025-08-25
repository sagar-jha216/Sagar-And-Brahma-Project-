from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.command_center import get_command_center_kpis
from typing import Optional, List
from datetime import date
import logging
from pydantic import BaseModel, Field

router = APIRouter()
logger = logging.getLogger(__name__)

class CommandCenterFilterParams(BaseModel):
    Region_Historical: Optional[str] = Field(None, alias="Region_Historical")
    Store_ID: Optional[List[str]] = Field(None, alias="Store_ID")
    Store_Channel: Optional[List[str]] = Field(None, alias="Store_Channel")
    Received_Date: Optional[date] = Field(None, alias="Received_Date")

    class Config:
        allow_population_by_field_name = True

@router.post("/command-center/kpis")
def get_command_center_kpi(filters: CommandCenterFilterParams, db: Session = Depends(get_db)):
    """Get Command Center KPIs with shrinkage and return analysis"""
    try:
        kpi_result = get_command_center_kpis(filters, db)
        return kpi_result
    except Exception as e:
        logger.error(f"Error generating command center KPIs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate command center KPIs: {str(e)}")