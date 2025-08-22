# Backend\app\controllers\analytics.py
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.models.inventory import Inventory
from typing import Dict, List

def get_shrinkage_analytics(db: Session) -> Dict:
    """
    Calculate shrinkage percentages by category and overall metrics
    """
    
    # Query shrinkage by category - use correct attribute names
    category_data = db.query(
        Inventory.Category,
        func.sum(Inventory.System_Quantity_Received).label('total_received'),
        func.sum(
            func.coalesce(Inventory.Number_Damaged_Units, 0) + 
            func.coalesce(Inventory.Number_Dump_Units, 0) + 
            func.coalesce(Inventory.Number_Expired_Units, 0)
        ).label('total_shrinkage'),
        func.sum(func.coalesce(Inventory.Difference_System_Actual, 0)).label('total_in_transit_loss')
    ).filter(
        Inventory.Category.isnot(None),
        Inventory.System_Quantity_Received > 0
    ).group_by(Inventory.Category).all()
    
    # Calculate category shrinkage percentages
    categories = []
    for row in category_data:
        shrinkage_pct = (row.total_shrinkage / row.total_received) * 100 if row.total_received > 0 else 0
        categories.append({
            "category": row.Category,
            "shrinkage_percentage": round(shrinkage_pct, 1)
        })
    
    # FIXED: Map database categories to frontend expected names
    category_mapping = {
        "Fresh Produce": "Produce (Fresh)",  # Fixed mapping
        "Dry Goods": "Dry Goods", 
        "General Merchandise": "General Merchandise"
    }
    
    # Ensure all expected categories are present
    expected_categories = ["Produce (Fresh)", "Dry Goods", "General Merchandise"]
    result_categories = {}
    
    for cat in categories:
        mapped_name = category_mapping.get(cat["category"], cat["category"])
        if mapped_name in expected_categories:
            result_categories[mapped_name] = cat["shrinkage_percentage"]
    
    # Fill missing categories with 0
    for expected in expected_categories:
        if expected not in result_categories:
            result_categories[expected] = 0.0
    
    # Calculate overall in-transit loss rate - use absolute value for differences
    overall_stats = db.query(
        func.sum(Inventory.System_Quantity_Received).label('total_received'),
        func.sum(func.abs(func.coalesce(Inventory.Difference_System_Actual, 0))).label('total_in_transit_loss')
    ).filter(
        Inventory.System_Quantity_Received > 0
    ).first()
    
    in_transit_loss_rate = 0.0
    if overall_stats and overall_stats.total_received and overall_stats.total_received > 0:
        in_transit_loss_rate = (overall_stats.total_in_transit_loss / overall_stats.total_received) * 100
    
    return {
        "shrinkage_by_category": result_categories,
        "in_transit_loss_rate": round(in_transit_loss_rate, 1)
    }