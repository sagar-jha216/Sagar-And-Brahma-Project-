from sqlalchemy.orm import Session
from sqlalchemy import func, case, desc
from app.models.inventory import Inventory
from app.models.returns import Return
from app.models.stores import Store
from app.utils.dashboard_filters import apply_inventory_filters
from typing import Optional, Dict
from datetime import date

def get_dashboard_kpis(
    db: Session,
    category: Optional[str] = None,
    region: Optional[str] = None,
    store_id: Optional[str] = None,
    time_period: Optional[date] = None,
    sub_category: Optional[str] = None,
    store_channel: Optional[str] = None
) -> Dict:

    # Apply shared filters
    query, db_category, db_region = apply_inventory_filters(
        db=db,
        category=category,
        region=region,
        store_id=store_id,
        time_period=time_period,
        sub_category=sub_category,
        store_channel=store_channel
    )

    # 1. Stock Inventory Accuracy %
    accuracy_data = query.with_entities(
        func.sum(Inventory.System_Quantity_Received).label('total_system'),
        func.sum(Inventory.Actual_Quantity_Received).label('total_actual')
    ).first()
    stock_accuracy = (accuracy_data.total_actual / accuracy_data.total_system * 100) if accuracy_data.total_system else 0.0

    # 2. Damaged %
    damaged_data = query.with_entities(
        func.sum(Inventory.System_Quantity_Received).label('total_received'),
        func.sum(Inventory.Number_Damaged_Units).label('total_damaged')
    ).first()
    damaged_percentage = (damaged_data.total_damaged / damaged_data.total_received * 100) if damaged_data.total_received else 0.0

    # 3. Dump %
    dump_data = query.with_entities(
        func.sum(Inventory.System_Quantity_Received).label('total_received'),
        func.sum(Inventory.Number_Dump_Units).label('total_dump')
    ).first()
    dump_percentage = (dump_data.total_dump / dump_data.total_received * 100) if dump_data.total_received else 0.0

    # 4. Aged Inventory %
    aged_data = query.with_entities(
        func.count(Inventory.SKU_ID).label('total_items'),
        func.sum(case((Inventory.Inventory_Age_Days > 7, 1), else_=0)).label('aged_items')
    ).first()
    aged_percentage = (aged_data.aged_items / aged_data.total_items * 100) if aged_data.total_items else 0.0

    # 5. Expired %
    expired_data = query.with_entities(
        func.sum(Inventory.System_Quantity_Received).label('total_received'),
        func.sum(Inventory.Number_Expired_Units).label('total_expired')
    ).first()
    expired_percentage = (expired_data.total_expired / expired_data.total_received * 100) if expired_data.total_received else 0.0

    # 6. Shrinkage % to SKU
    total_items = query.with_entities(func.count(Inventory.SKU_ID)).scalar()
    top_30_items = min(30, total_items) if total_items else 0
    shrinkage_to_sku = (top_30_items / total_items * 100) if total_items else 0.0

    # 7. Return %
    return_query = db.query(Return)
    if db_category:
        return_query = return_query.filter(Return.category == db_category)
    if db_region:
        return_query = return_query.join(Store, Return.store_id == Store.Store_ID).filter(Store.Store_Region == db_region)
    if store_id:
        return_query = return_query.filter(Return.store_id == store_id)
    if time_period:
        return_query = return_query.filter(Return.return_date == time_period)
    if sub_category:
        if sub_category == "Fruits & Vegetables":
            return_query = return_query.filter(
                Return.product_name.contains("Fruit") |
                Return.product_name.contains("Vegetable") |
                Return.product_name.contains("Apple") |
                Return.product_name.contains("Banana") |
                Return.product_name.contains("Orange") |
                Return.product_name.contains("Greens") |
                Return.product_name.contains("Leafy")
            )
        else:
            return_query = return_query.filter(Return.product_name.contains(sub_category))

    return_data = return_query.with_entities(func.sum(Return.quantity_returned).label('total_returned')).first()
    total_sold = query.with_entities(func.sum(Inventory.Unit_Sold).label('total_sold')).first()
    return_percentage = (return_data.total_returned / total_sold.total_sold * 100) if total_sold.total_sold and return_data.total_returned else 0.0

    return {
        "stock_inventory_accuracy": round(stock_accuracy, 1),
        "damaged_percentage": round(damaged_percentage, 1),
        "dump_percentage": round(dump_percentage, 1),
        "aged_inventory_percentage": round(aged_percentage, 1),
        "products_expired_percentage": round(expired_percentage, 1),
        "shrinkage_to_sku_percentage": round(shrinkage_to_sku, 1),
        "return_percentage": round(return_percentage, 1),
        "filters_applied": {
            "category": category,
            "db_category": db_category,
            "region": region,
            "db_region": db_region,
            "store_id": store_id,
            "time_period": time_period.isoformat() if time_period else None,
            "sub_category": sub_category,
            "store_channel": store_channel,
            "total_records_found": total_items
        }
    }
