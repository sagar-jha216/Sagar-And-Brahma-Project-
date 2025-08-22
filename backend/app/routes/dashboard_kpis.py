from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.dashboard_kpis import get_dashboard_kpis
from typing import Optional
from datetime import date
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/kpis/formatted")
def get_formatted_dashboard_kpis(
    category: Optional[str] = Query(None, description="Product category filter"),
    region: Optional[str] = Query(None, description="Store region filter"),
    store_id: Optional[str] = Query(None, description="Specific store ID"),
    time_period: Optional[date] = Query(None, description="Filter by Received_Date (YYYY-MM-DD)"),
    sub_category: Optional[str] = Query(None, description="Sub category filter"),
    store_channel: Optional[str] = Query(None, description="Store channel filter (future use)"),
    db: Session = Depends(get_db)
):
    """
    Returns 7 formatted KPI metrics for the dashboard.
    """
    try:
        kpis = get_dashboard_kpis(
            db=db,
            category=category,
            region=region,
            store_id=store_id,
            time_period=time_period,
            sub_category=sub_category,
            store_channel=store_channel
        )

        formatted_kpis = [
            {
                "id": "stock-accuracy",
                "title": "Stock Inventory Accuracy %",
                "value": f"{kpis['stock_inventory_accuracy']}%",
                "percentage": kpis['stock_inventory_accuracy'],
                "doughnutchartData": [kpis['stock_inventory_accuracy'], 100 - kpis['stock_inventory_accuracy']]
            },
            {
                "id": "damaged",
                "title": "Damaged %",
                "value": f"{kpis['damaged_percentage']}%",
                "percentage": kpis['damaged_percentage'],
                "doughnutchartData": [kpis['damaged_percentage'], 100 - kpis['damaged_percentage']]
            },
            {
                "id": "dump",
                "title": "Dump %",
                "value": f"{kpis['dump_percentage']}%",
                "percentage": kpis['dump_percentage'],
                "doughnutchartData": [kpis['dump_percentage'], 100 - kpis['dump_percentage']]
            },
            {
                "id": "aged-inventory",
                "title": "Aged Inventory %",
                "value": f"{kpis['aged_inventory_percentage']}%",
                "percentage": kpis['aged_inventory_percentage'],
                "doughnutchartData": [kpis['aged_inventory_percentage'], 100 - kpis['aged_inventory_percentage']]
            },
            {
                "id": "products-expired",
                "title": "% Of Products Expired",
                "value": f"{kpis['products_expired_percentage']}%",
                "percentage": kpis['products_expired_percentage'],
                "doughnutchartData": [kpis['products_expired_percentage'], 100 - kpis['products_expired_percentage']]
            },
            {
                "id": "shrinkage-sku",
                "title": "Shrinkage% to SKU",
                "value": f"{kpis['shrinkage_to_sku_percentage']}%",
                "percentage": kpis['shrinkage_to_sku_percentage'],
                "labelSKUDetails": 30
            },
            {
                "id": "return",
                "title": "Return %",
                "value": f"{kpis['return_percentage']}%",
                "percentage": kpis['return_percentage'],
                "doughnutchartData": [kpis['return_percentage'], 100 - kpis['return_percentage']]
            }
        ]

        return {
            "status": "success",
            "message": "Dashboard KPIs retrieved successfully",
            "kpis": formatted_kpis,
            "filters_applied": kpis["filters_applied"]
        }

    except Exception as e:
        logger.error(f"Error retrieving dashboard KPIs: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
