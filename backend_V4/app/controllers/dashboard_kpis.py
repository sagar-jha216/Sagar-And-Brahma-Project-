from sqlalchemy.orm import Session
from sqlalchemy import func, case, desc
from app.models.inventory import Inventory
from app.models.returns import Return
from app.models.stores import Store
from app.utils.dashboard_filters import apply_inventory_filters
from typing import Optional, Dict
from datetime import date
import pandas as pd

def apply_filters(df, filters):
    df_filtered = df.copy()
    if filters.Category:
        df_filtered = df_filtered[df_filtered["Category"] == filters.Category]
    if filters.Sub_Category:
        df_filtered = df_filtered[df_filtered["Sub_Category"] == filters.Sub_Category]
    if filters.Region_Historical:
        df_filtered = df_filtered[df_filtered["Region_Historical"] == filters.Region_Historical]
    if filters.Store_ID:
        df_filtered = df_filtered[df_filtered["Store_ID"].isin(filters.Store_ID)]
    if filters.Store_Channel:
        df_filtered = df_filtered[df_filtered["Store_Channel"].isin(filters.Store_Channel)]
    # if filters.Start_Date:
    #     df_filtered = df_filtered[pd.to_datetime(df_filtered["Received_Date"]) >= pd.to_datetime(filters.Start_Date)]
    # if filters.End_Date:
    #     df_filtered = df_filtered[pd.to_datetime(df_filtered["Received_Date"]) <= pd.to_datetime(filters.End_Date)]
    return df_filtered

def get_dashboard_kpis(filters, db: Session):
    # Query all data from inventory and returns
    inve_records = db.query(Inventory).all()
    returns_records = db.query(Return).all()
    # Convert to DataFrames
    df_inve = pd.DataFrame([r.__dict__ for r in inve_records])
    df_returns = pd.DataFrame([r.__dict__ for r in returns_records])

    # Drop SQLAlchemy internal state column if present

    if '_sa_instance_state' in df_inve.columns:
        df_inve.pop('_sa_instance_state')

    # Apply filters
    filtered_df = apply_filters(df_inve, filters)
    
    def sum_by_key(df, key):
        return df[key].fillna(0).sum()

    def inventory_accuracy(df):
        system_qty = sum_by_key(df, "System_Quantity_Received")
        return (sum_by_key(df, "Actual_Quantity_Received") / system_qty * 100) if system_qty else 0

    def damaged_pct(df):
        actual_qty = sum_by_key(df, "Actual_Quantity_Received")
        return (sum_by_key(df, "Number_Damaged_Units") / actual_qty * 100) if actual_qty else 0

    def dump_pct(df):
        actual_qty = sum_by_key(df, "Actual_Quantity_Received")
        return (sum_by_key(df, "Number_Dump_Units") / actual_qty * 100) if actual_qty else 0

    def expired_pct(df):
        actual_qty = sum_by_key(df, "Actual_Quantity_Received")
        return (sum_by_key(df, "Number_Expired_Units") / actual_qty * 100) if actual_qty else 0

    def aged_pct(df):
        aged_df = df[df["Inventory_Status"].isin(["Expiry Approaching", "Critical - Expiring Soon"])]
        actual_qty = sum_by_key(df, "Actual_Quantity_Received")
        return (sum_by_key(aged_df, "Actual_Quantity_Received") / actual_qty * 100) if actual_qty else 0

    def return_pct(df_inv, df_ret):
        sold = sum_by_key(df_inv, "Unit_Sold")
        if filters.Category:
            df_ret = df_ret[df_ret["category"] == filters.Category]
        returned = sum_by_key(df_ret, "quantity_returned")
        return (returned / sold * 100) if sold else 0

    def shrinkage_pct(df):
        actual_qty = sum_by_key(df, "Actual_Quantity_Received")
        dump_units = sum_by_key(df, "Number_Dump_Units")
        damaged_units = sum_by_key(df, "Number_Damaged_Units")
        expired_units = sum_by_key(df, "Number_Expired_Units")

        total_shrinkage_units = dump_units + damaged_units + expired_units
        print(shrinkage_pct)
        return (total_shrinkage_units / actual_qty * 100) if actual_qty else 0






    return {
        "Category": filters.Category or "All",
        "Subcategory": filters.Sub_Category or "All",
        "Region": filters.Region_Historical or "All",
        "Inventory_Accuracy": round(inventory_accuracy(filtered_df), 2),
        "Damage_%": round(damaged_pct(filtered_df), 2),
        "Dump_%": round(dump_pct(filtered_df), 2),
        "Expired_%": round(expired_pct(filtered_df), 2),
        "Aged_%": round(aged_pct(filtered_df), 2),
        "Return_%": round(return_pct(filtered_df, df_returns), 2),
        "Shrinkage_%": round(shrinkage_pct(filtered_df), 2)
    }
