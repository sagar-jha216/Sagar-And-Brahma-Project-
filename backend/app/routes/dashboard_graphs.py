from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.dashboard_graphs import get_dashboard_graphs
from typing import Optional

router = APIRouter()

@router.get("/kpis/graphs")
def fetch_graphs(
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    store_id: Optional[str] = Query(None),
    time_period: Optional[str] = Query(None),
    sub_category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    graphs = get_dashboard_graphs(db, category, region, store_id, time_period, sub_category)
    return {
        "status": "success",
        "graphs": graphs,
        "filters": {
            "category": category,
            "region": region,
            "store_id": store_id,
            "time_period": time_period,
            "sub_category": sub_category
        }
    }
