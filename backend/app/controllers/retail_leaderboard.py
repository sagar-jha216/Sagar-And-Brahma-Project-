"""
Retail Leader Board API - Dynamic shrinkage calculation from database
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, case
from typing import List
from pydantic import BaseModel

from app.database import get_db, ProductMaster, Inventory, Returns, Store
from app.middleware.auth import verify_token

router = APIRouter()

class CategoryShrinkage(BaseModel):
    category: str
    shrinkage_percentage: float
    benchmark_low: float
    benchmark_median: float
    benchmark_high: float
    status: str  # "best", "median", "laggard"

class ShrinkageData(BaseModel):
    produce_fresh: CategoryShrinkage
    dry_goods: CategoryShrinkage
    general_merchandise: CategoryShrinkage
    in_transit_loss_rate: float

@router.get("/dashboard-summary")
async def get_dashboard_summary(
    username: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get complete dashboard metrics calculated from database"""
    
    # 1. Calculate actual shrinkage by category from waste components
    category_shrinkage = db.query(
        ProductMaster.category,
        func.avg(
            case(
                (Inventory.actual_quantity_received > 0,
                 ((Inventory.number_damaged_units + Inventory.number_dump_units + Inventory.number_expired_units) 
                  / Inventory.actual_quantity_received * 100)),
                else_=0
            )
        ).label('avg_shrinkage'),
        func.count(ProductMaster.sku_id).label('product_count'),
        func.sum(Inventory.current_stock * Inventory.cost_price).label('total_value')
    ).join(
        Inventory, ProductMaster.sku_id == Inventory.sku_id
    ).group_by(ProductMaster.category).all()
    
    # 2. Store performance rankings with calculated shrinkage
    store_performance = db.query(
        Store.store_id,
        Store.store_name,
        Store.store_city,
        func.avg(
            case(
                (Inventory.actual_quantity_received > 0,
                 ((Inventory.number_damaged_units + Inventory.number_dump_units + Inventory.number_expired_units) 
                  / Inventory.actual_quantity_received * 100)),
                else_=0
            )
        ).label('avg_shrinkage'),
        func.count(Returns.id).label('return_count'),
        Store.performance_score
    ).outerjoin(
        Inventory, Store.store_id == Inventory.store_id
    ).outerjoin(
        Returns, Store.store_id == Returns.store_id
    ).group_by(Store.store_id).order_by(
        desc(Store.performance_score)
    ).limit(10).all()
    
    # 3. Calculate overall metrics
    total_inventory_value = db.query(
        func.sum(Inventory.current_stock * Inventory.cost_price)
    ).scalar() or 0
    
    avg_shrinkage = db.query(
        func.avg(
            case(
                (Inventory.actual_quantity_received > 0,
                 ((Inventory.number_damaged_units + Inventory.number_dump_units + Inventory.number_expired_units) 
                  / Inventory.actual_quantity_received * 100)),
                else_=0
            )
        )
    ).scalar() or 0
    
    total_returns = db.query(func.count(Returns.id)).scalar() or 0
    total_products = db.query(func.count(ProductMaster.sku_id)).scalar() or 0
    
    return_rate = (total_returns / total_products * 100) if total_products > 0 else 0
    
    return {
        "summary": {
            "total_inventory_value": round(total_inventory_value, 2),
            "overall_shrinkage_rate": round(avg_shrinkage, 2),
            "total_return_rate": round(return_rate, 2),
            "total_stores": db.query(func.count(Store.store_id)).scalar(),
            "total_products": total_products
        },
        "category_performance": [
            {
                "category": row.category,
                "shrinkage_percentage": round(float(row.avg_shrinkage or 0), 2),
                "product_count": row.product_count,
                "inventory_value": round(float(row.total_value or 0), 2)
            } for row in category_shrinkage
        ],
        "top_stores": [
            {
                "store_id": row.store_id,
                "store_name": row.store_name,
                "city": row.store_city,
                "shrinkage_rate": round(float(row.avg_shrinkage or 0), 2),
                "return_count": row.return_count or 0,
                "performance_score": round(float(row.performance_score or 0), 2)
            } for row in store_performance
        ]
    }

@router.get("/shrinkage-metrics")
async def get_shrinkage_metrics(
    username: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get shrinkage metrics calculated dynamically from database waste data"""
    
    # Calculate actual shrinkage by category from waste components
    category_stats = db.query(
        ProductMaster.category,
        func.avg(
            case(
                (Inventory.actual_quantity_received > 0,
                 ((Inventory.number_damaged_units + Inventory.number_dump_units + Inventory.number_expired_units) 
                  / Inventory.actual_quantity_received * 100)),
                else_=0
            )
        ).label('avg_shrinkage'),
        func.count(Inventory.id).label('item_count')
    ).join(
        Inventory, ProductMaster.sku_id == Inventory.sku_id
    ).group_by(ProductMaster.category).all()
    
    # Calculate actual in-transit loss rate from shipment discrepancies
    total_system_qty = db.query(func.sum(Inventory.system_quantity_received)).scalar() or 0
    total_actual_qty = db.query(func.sum(Inventory.actual_quantity_received)).scalar() or 0
    in_transit_loss = ((total_system_qty - total_actual_qty) / total_system_qty * 100) if total_system_qty > 0 else 0
    
    # Define benchmarks (including in-transit loss)
    benchmarks = {
        'Produce': {'best': 3, 'median': 7, 'laggard': 12},
        'Dry Goods': {'best': 3.5, 'median': 6.5, 'laggard': 12},
        'General Merchandise': {'best': 1, 'median': 1.8, 'laggard': 2.5}
    }
    
    # In-transit loss benchmarks (industry standards)
    transit_benchmarks = {'best': 2, 'median': 4, 'laggard': 7}
    
    def get_status(value, benchmark):
        if value <= benchmark['best']:
            return "best"
        elif value <= benchmark['median']:
            return "median"
        else:
            return "laggard"
    
    # Build categories with actual data
    categories = []
    for stat in category_stats:
        category = stat.category
        shrinkage = round(float(stat.avg_shrinkage or 0), 1)
        
        # Map category names
        display_name = category
        if 'Produce' in category or 'Fresh' in category:
            display_name = "Produce (Fresh)"
            bench = benchmarks.get('Produce', benchmarks['General Merchandise'])
        elif 'Dry' in category:
            display_name = "Dry Goods"
            bench = benchmarks.get('Dry Goods', benchmarks['General Merchandise'])
        else:
            display_name = "General Merchandise"
            bench = benchmarks.get('General Merchandise')
        
        categories.append({
            "name": display_name,
            "percentage": shrinkage,
            "status": get_status(shrinkage, bench),
            "benchmarks": bench
        })
    
    return {
        "categories": categories,
        "in_transit_loss_rate": round(in_transit_loss, 1),
        "transit_status": get_status(in_transit_loss, transit_benchmarks),
        "transit_benchmarks": transit_benchmarks,
        "benchmarking_source": "NRF"
    }