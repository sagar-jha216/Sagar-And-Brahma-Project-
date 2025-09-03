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
   

    def return_pct(df_inv, df_ret):
        sold = sum_by_key(df_inv, "Unit_Sold")
        if filters.Category:
            df_ret = df_ret[df_ret["category"] == filters.Category]
        returned = sum_by_key(df_ret, "quantity_returned")
        return (returned / sold * 100) if sold else 0
    

    def kpi_percentage_change(df, category, col_name, ref_date=None):
        
        # filtered = data[data["Category"] == category].copy()
        filtered = df;

        filtered["received_date"] = pd.to_datetime(filtered["Received_Date"])

        # determine "today"
        if ref_date is None:
            today = filtered["received_date"].max().normalize()
        else:
            today = pd.to_datetime(ref_date).normalize()

        # logic for comparison date
        if category == "Fresh Produce":
            compare_date = today - pd.Timedelta(days=1)
        else:  # Dry Goods & General Merchandise
            compare_date = (today - pd.offsets.MonthEnd(1)) #today - pd.DateOffset(months=1)

        # helper to compute %
        def calc_pct(df):
            actual_qty = df["Actual_Quantity_Received"].sum()
            kpi_qty = df[col_name].sum()
            return (kpi_qty / actual_qty * 100) if actual_qty > 0 else 0

        today_pct = calc_pct(filtered[filtered["received_date"] <= today])
        compare_pct = calc_pct(filtered[filtered["received_date"] <= compare_date])

        # % change (today → compare date)
        if today_pct == 0:
            pct_change = None if compare_pct == 0 else float("inf")
        else:
            pct_change = ((compare_pct - today_pct) / today_pct) * 100

        return {
            "today_pct": round(today_pct,2),
            "compare_pct": round(compare_pct or 0),
            "pct_change": round(pct_change or 0),
            "compare_basis": "yesterday" if category == "Fresh Produce" else "month"
        }
    
    #aged_pct_by_category
    def aged_percentage(data, category, ref_date=None):
        aged_statuses = ["Expiry Approaching", "Critical - Expiring Soon"]
        data = data[(data["Category"] == category)].copy()
        data["received_date"] = pd.to_datetime(data["Received_Date"])
        filtered = data[(data["Inventory_Status"].isin(aged_statuses)) ].copy()

        # Determine "today"
        if ref_date is None:
            today = data["received_date"].max().normalize()
        else:
            today = pd.to_datetime(ref_date).normalize()

        # Determine comparison date
        if category == "Fresh Produce":
            compare_date = today - pd.Timedelta(days=1)
        else:  # Dry Goods & General Merchandise
            compare_date = today - pd.offsets.MonthEnd(1)

        # Helper to calculate percentage
        def calc_pct(df_1, df_2):
            actual_qty = df_1["Actual_Quantity_Received"].sum()
            aged_qty = df_2["Actual_Quantity_Received"].sum()
            return (aged_qty / actual_qty * 100) if actual_qty > 0 else 0

        # Calculate today's and comparison percentages
        today_pct = calc_pct(data[data["received_date"] <= today],
                            filtered[filtered["received_date"] <= today])
        compare_pct = calc_pct(data[data["received_date"] <= compare_date],
                            filtered[filtered["received_date"] <= compare_date])

        # Calculate percentage change
        if today_pct == 0:
            pct_change = None if compare_pct == 0 else float("inf")
        else:
            pct_change = ((compare_pct - today_pct) / today_pct) * 100

        return {
            "today_pct": round(today_pct, 2),
            "compare_pct": round(compare_pct, 2),
            "pct_change": round(pct_change, 2) if pct_change is not None else None,
            "compare_basis": "yesterday" if category == "Fresh Produce" else "month"
        }
        


    def shrinkage_pct(df, sku_col="SKU_ID", shrink_col="Difference_System_Actual", target_pct=80):
        
        # Aggregate shrinkage per SKU
        shrink_by_sku = df.groupby(sku_col)[shrink_col].sum().reset_index()
        
        # Sort SKUs by shrinkage in descending order
        shrink_by_sku = shrink_by_sku.sort_values(shrink_col, ascending=False)
        
        # Calculate cumulative shrinkage percentage
        shrink_by_sku["CUM_SHRINK_PCT"] = (
            shrink_by_sku[shrink_col].cumsum() / shrink_by_sku[shrink_col].sum() * 100
        )
        
        # Count SKUs needed to reach the target shrinkage percentage
        sku_count = (shrink_by_sku["CUM_SHRINK_PCT"] <= target_pct).sum()
        
        # Calculate SKU percentage
        total_skus = shrink_by_sku[sku_col].nunique()
        sku_pct = sku_count / total_skus * 100 if total_skus else 0

        return int(sku_count)
        # Optional detailed return:
        # return {
        #     "target_shrinkage_pct": target_pct,
        #     "sku_count": sku_count,
        #     "sku_pct": sku_pct,
        #     "total_skus": total_skus
        # }


    def inventory_age_buckets(df):
        # Define bucket labels
        buckets = {
            "0-30 days": 0,
            "31-60 days": 0,
            "61-90 days": 0,
            "91-180 days": 0,
            "181-365 days": 0
        }

        # Iterate through the DataFrame
        for age in df["Inventory_Age_Days"]:
            if 0 <= age <= 30:
                buckets["0-30 days"] += 1
            elif 31 <= age <= 60:
                buckets["31-60 days"] += 1
            elif 61 <= age <= 90:
                buckets["61-90 days"] += 1
            elif 91 <= age <= 180:
                buckets["91-180 days"] += 1
            elif 181 <= age <= 365:
                buckets["181-365 days"] += 1

        return buckets





    return {
        "Category": filters.Category or "All",
        "Subcategory": filters.Sub_Category or "All",
        "Region": filters.Region_Historical or "All",
        "Inventory_Age_Buckets": inventory_age_buckets(filtered_df),
        # "Damage_%": round(damaged_pct(filtered_df), 2),
        # "Dump_%": round(dump_pct(filtered_df), 2),
        # "Expired_%": round(expired_pct(filtered_df), 2),
        # "Aged_%": round(aged_pct(filtered_df), 2),
        "Inventory_Age_Buckets": inventory_age_buckets(filtered_df) ,
        "Return_%": round(return_pct(filtered_df, df_returns), 2),
        "Shrinkage": round(shrinkage_pct(filtered_df), 2),
        "inventory_accuracy":round(inventory_accuracy(filtered_df),2),
        "kpi_result" :{
        "kpi_percentage_change_Number_Damaged_Units": kpi_percentage_change(filtered_df, filters.Category, "Number_Damaged_Units"),
        "kpi_percentage_change_Number_Dump_Units": kpi_percentage_change(filtered_df, filters.Category, "Number_Dump_Units"),
        "kpi_percentage_change_Number_Expired_Units": kpi_percentage_change(filtered_df, filters.Category, "Number_Expired_Units")
                     },
        "aged_percentage":aged_percentage(filtered_df, filters.Category),             
    }
