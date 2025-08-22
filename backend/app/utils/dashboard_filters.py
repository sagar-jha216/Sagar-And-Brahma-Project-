from sqlalchemy.orm import Session
from sqlalchemy import or_, and_,case,desc
from app.models.inventory import Inventory
from typing import Optional, Tuple

def apply_inventory_filters(
    db: Session,
    category: Optional[str],
    region: Optional[str],
    store_id: Optional[str],
    time_period: Optional[str],
    sub_category: Optional[str],
    store_channel: Optional[str] = None  # Placeholder for future use
) -> Tuple:
    # Category mapping from frontend to database
    category_mapping = {
        "Produce (Fresh)": "Fresh Produce",
        "Dry Goods": "Dry Goods",
        "General Merchandise": "General Merchandise"
    }
    db_category = category_mapping.get(category, category) if category else None

    # Region mapping
    region_mapping = {
        "East": "East",
        "West": "West",
        "North": "North",
        "South": "South"
    }
    db_region = region_mapping.get(region, region) if region else None

    query = db.query(Inventory)
    filters = []

    # 1. Category filter
    if db_category:
        filters.append(Inventory.Category == db_category)

    # 2. Region filter
    if db_region:
        filters.append(Inventory.Region_Historical == db_region)

    # 3. Store ID filter
    if store_id:
        filters.append(Inventory.Store_ID == store_id)

    # 4. Time period filter
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

    # 6. Store channel filter (not implemented yet)
    # You can add logic here when mapping is available

    if filters:
        query = query.filter(and_(*filters))

    return query, db_category, db_region
