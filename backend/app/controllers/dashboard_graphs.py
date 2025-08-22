from app.utils.dashboard_filters import apply_inventory_filters
from app.utils.analytics import (
    wastage_by_merch_cat,
    waste_pct_of_cogs,
    suppliers_highest_shrinkage,
    non_sellable_inventory,
    shrink_inv_ratio,
    sku_highest_shrinkage
)
import pandas as pd

def get_dashboard_graphs(db, category, region, store_id, time_period, sub_category):
    query, db_category, db_region = apply_inventory_filters(
        db, category, region, store_id, time_period, sub_category
    )
    df = pd.read_sql(query.statement, db.bind)

    # Call your graph functions here
    return {
        "wastage_by_merch_category": wastage_by_merch_cat(df, db_category),
        "waste_pct_of_cogs": waste_pct_of_cogs(df, db_category),
        "suppliers_highest_shrinkage": suppliers_highest_shrinkage(df, db_category),
        "non_sellable_inventory": non_sellable_inventory(df, db_category),
        "sales_vs_shrinkage_vs_salvage": shrink_inv_ratio(df, db_category),
        "top_10_sku_shrinkage": sku_highest_shrinkage(df, db_category)
    }
