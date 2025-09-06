from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.Retail_Leader_Board_KPIs import RetailKPICreate, RetailKPIResponse
from app.controllers.Retail_Leader_Board_KPIs import create_kpi, get_all_kpis

router = APIRouter()

@router.post("/kpi/", response_model=RetailKPIResponse)
def add_kpi(kpi: RetailKPICreate, db: Session = Depends(get_db)):
    return create_kpi(db, kpi)

@router.get("/kpi/", response_model=list[RetailKPIResponse])
def read_kpis(db: Session = Depends(get_db)):
    return get_all_kpis(db)
