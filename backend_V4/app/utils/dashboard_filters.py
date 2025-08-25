from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models.inventory import Inventory
from typing import Optional, Tuple
from sqlalchemy.orm.query import Query

def apply_inventory_filters(
    db: Session,
    category: Optional[str],
    region: Optional[str],
    store_id: Optional[str],
    time_period: Optional[str],
    sub_category: Optional[str],
    store_channel: Optional[str] = None
) -> Tuple[Query, Optional[str], Optional[str]]:
    # Mappings
    category_mapping = {
        "Produce (Fresh)": "Produce (Fresh)",
        "Dry Goods": "Dry Goods",
        "General Merchandise": "General Merchandise"
    }
    region_mapping = {
        "East": "East",
        "West": "West",
        "North": "North",
        "South": "South"
    }

    db_category = category_mapping.get(category, category) if category else None
    db_region = region_mapping.get(region, region) if region else None

    query = db.query(Inventory)
    filters = []

    # 1. Category filter
    if db_category:
        filters.append(Inventory.Category == db_category)

    # 2. Region filter
    if db_region:
        filters.append(Inventory.Region_Historical == db_region)

    # 3. Store ID filter (supports comma-separated values)
    if store_id:
        store_ids = [s.strip() for s in store_id.split(',') if s.strip()]
        if store_ids:
            filters.append(Inventory.Store_ID.in_(store_ids))

    # 4. Time period filter (expects 'YYYY-MM-DD')
    if time_period:
        filters.append(Inventory.Received_Date == time_period)

    # 5. Sub-category filter
    if sub_category:
        if sub_category == "Fruits & Vegetables":
            filters.append(or_(
                Inventory.Product_Name.contains("Fruit"),
                Inventory.Product_Name.contains("Vegetable"),
                Inventory.Product_Name.contains("Apple"),
                Inventory.Product_Name.contains("Banana"),
                Inventory.Product_Name.contains("Orange"),
                Inventory.Product_Name.contains("Greens"),
                Inventory.Product_Name.contains("Leafy")
            ))
        else:
            filters.append(Inventory.Product_Name.contains(sub_category))

    # 6. Store channel filter (supports comma-separated values)
    if store_channel:
        channels = [c.strip() for c in store_channel.split(',') if c.strip()]
        if channels:
            filters.append(Inventory.Store_Channel.in_(channels))

    # Apply filters
    print(filters)
    if filters:
        query = query.filter(and_(*filters))

    return query, db_category, db_region
