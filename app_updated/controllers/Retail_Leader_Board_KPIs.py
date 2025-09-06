from sqlalchemy.orm import Session
from app.models.Retail_Leader_Board_KPIs import RetailKPI
from app.schemas.Retail_Leader_Board_KPIs import RetailKPICreate

def create_kpi(db: Session, kpi: RetailKPICreate):
    db_kpi = RetailKPI(**kpi.dict())
    db.add(db_kpi)
    db.commit()
    db.refresh(db_kpi)
    return db_kpi

def get_all_kpis(db: Session):
    return db.query(RetailKPI).all()
