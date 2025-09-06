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
        df_filtered = df_filtered[df_filtered["Sub_Category"].isin(filters.Sub_Category)]
    if filters.Region_Historical:
        df_filtered = df_filtered[df_filtered["Region_Historical"] == filters.Region_Historical]
    if filters.Store_ID:
        df_filtered = df_filtered[df_filtered["Store_ID"].isin(filters.Store_ID)]
    if filters.Store_Channel:
        df_filtered = df_filtered[df_filtered["Store_Channel"].isin(filters.Store_Channel)]
    if filters.Received_Date:
        df_filtered = df_filtered[pd.to_datetime(df_filtered["Received_Date"]).dt.date <= filters.Received_Date]
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
   
    #  This is old logic (currentely we are not using these)
    # def damaged_pct(df):
    #     actual_qty = sum_by_key(df, "Actual_Quantity_Received")
    #     return (sum_by_key(df, "Number_Damaged_Units") / actual_qty * 100) if actual_qty else 0

    # def dump_pct(df):
    #     actual_qty = sum_by_key(df, "Actual_Quantity_Received")
    #     return (sum_by_key(df, "Number_Dump_Units") / actual_qty * 100) if actual_qty else 0

    # def expired_pct(df):
    #     actual_qty = sum_by_key(df, "Actual_Quantity_Received")
    #     return (sum_by_key(df, "Number_Expired_Units") / actual_qty * 100) if actual_qty else 0

    # def aged_pct(df):
    #     aged_df = df[df["Inventory_Status"].isin(["Expiry Approaching", "Critical - Expiring Soon"])]
    #     actual_qty = sum_by_key(df, "Actual_Quantity_Received")
    #     return (sum_by_key(aged_df, "Actual_Quantity_Received") / actual_qty * 100) if actual_qty else 0

    def return_pct(df_inv, df_ret):
        # Check if returns DataFrame is empty
        if df_ret.empty:
            return 0

        # Rename returns columns to match inventory for merge
        # 
        # Merge inventory and returns tables
        #merged_df = pd.merge(df_inv, df_ret_renamed, on=['SKU_ID', 'Store_ID', 'Category', 'Sub_Category', 'Cost_Price_CP'], how='left', suffixes=('_inv', '_ret')).dropna()
        df_ret_renamed = df_ret.rename(columns={
            'sku_id': 'SKU_ID',
            'store_id': 'Store_ID',
            'category': 'Category',
            'sub_category': 'Sub_Category',
            #'store_region': 'Region'
        })
 
 
        # merged_df = pd.merge(df_inv[['SKU_ID', 'Store_ID', 'Category', 'Received_Date', 'Sub_Category', 'Region_Historical', 'Cost_Price_CP', 'Unit_Sold']],
        #                     df_ret_renamed[['SKU_ID', 'Store_ID', 'Category', 'Sub_Category', 'Cost_Price_CP', 
        #                         'quantity_returned', 'return_date']], on = ['SKU_ID', 'Store_ID', 'Category', 'Sub_Category', 'Cost_Price_CP'], how='left', indicator=True)
        
        # Updated line for merged_df creation
        merged_df = pd.merge(df_inv[['SKU_ID', 'Store_ID', 'Category', 'Received_Date', 'Sub_Category', 'Region_Historical', 'Cost_Price_CP', 'Unit_Sold', 'Store_Channel']], df_ret_renamed[['SKU_ID', 'Store_ID', 'Category', 'Sub_Category', 'Cost_Price_CP', 'quantity_returned', 'return_date']], on=['SKU_ID', 'Store_ID', 'Category', 'Sub_Category', 'Cost_Price_CP'], how='left', indicator=True)        
        inv_df = df_inv.copy()
        #merged_df = apply_filters(merged_df, filters)
        # Apply all five filters to the merged table
        if filters.Category:
            merged_df = merged_df[merged_df["Category"] == filters.Category]
            inv_df = inv_df[inv_df["Category"] == filters.Category]

        if filters.Sub_Category:
            merged_df = merged_df[merged_df["Sub_Category"].isin(filters.Sub_Category)]
            inv_df = inv_df[inv_df["Sub_Category"].isin(filters.Sub_Category)]
        
        if filters.Region_Historical:
            merged_df = merged_df[merged_df["Region_Historical"] == filters.Region_Historical]
            inv_df = inv_df[inv_df["Region_Historical"] == filters.Region_Historical]

        if filters.Store_ID:
            merged_df = merged_df[merged_df["Store_ID"].isin(filters.Store_ID)]
            inv_df = inv_df[inv_df["Store_ID"].isin(filters.Store_ID)]

        if filters.Store_Channel:
            merged_df = merged_df[merged_df["Store_Channel"].isin(filters.Store_Channel)]
            inv_df = inv_df[inv_df["Store_Channel"].isin(filters.Store_Channel)]

        # if filters.Received_Date:
        #     merged_df = merged_df[pd.to_datetime(merged_df["return_date"]).dt.date <= filters.Received_Date]

        #sold = sum_by_key(merged_df, "Unit_Sold")
        
        if filters.Received_Date:
            df_ret_dates = pd.to_datetime(merged_df["return_date"], errors='coerce')
            df_rec_dates = pd.to_datetime(merged_df["Received_Date"], errors='coerce')
            df_rec_dates1 = pd.to_datetime(inv_df["Received_Date"], errors='coerce')
            merged_df = merged_df[(df_ret_dates <= pd.to_datetime(filters.Received_Date))]
            merged_df = merged_df[(df_rec_dates <= pd.to_datetime(filters.Received_Date))]
            inv_df = inv_df[(df_rec_dates1 <= pd.to_datetime(filters.Received_Date))]

        # # Handle empty dataframe
        # if merged_df.empty:
        #     return {
        #         "today_pct": 0.0,
        #         "compare_pct": 0.0,
        #         "pct_change": 0.0,
        #         "compare_basis": "month"
        #     }

        # # determine "today"
        # if ref_date is None:
        #     max_date = merged_df["return_date"].max()
        #     if pd.isna(max_date):  # Check if max_date is NaT
        #         today = pd.Timestamp.now().normalize()
        #     else:
        #         today = max_date.normalize()
        # else:
        #     today = pd.to_datetime(ref_date).normalize()

        # # logic for comparison date
        # compare_date = (today - pd.offsets.MonthEnd(1)) #today - pd.DateOffset(months=1)
        # print(compare_date, today)
        # # helper to compute %
        # def calc_pct(inv_df,merged_df):
        #     actual_qty = sum_by_key(inv_df, "Unit_Sold")
        #     kpi_qty = sum_by_key(merged_df, "quantity_returned")
        #     return (kpi_qty / actual_qty * 100) if actual_qty > 0 else 0

        # today_pct = calc_pct(merged_df[df_ret_dates.normalize() <= today], inv_df[df_rec_dates1.normalize() <= today])
        # compare_pct = calc_pct(merged_df[df_ret_dates.normalize() <= compare_date],inv_df[df_rec_dates1.normalize() <= compare_date])

        # # % change (today → compare date)
        # if today_pct == 0:
        #     pct_change = 0.0 if compare_pct == 0 else float("inf")
        # else:
        #     pct_change = (compare_pct - today_pct)

        # return {
        #     "today_pct": round(today_pct, 2),
        #     "compare_pct": round(compare_pct or 0, 2),
        #     "pct_change": round(pct_change if pct_change != float("inf") else 0.0, 2),
        #     "compare_basis": "month"
        # }
        
        
        sold = sum_by_key(inv_df, "Unit_Sold")

        # if filters.Received_Date:
        #     df_ret_dates = pd.to_datetime(merged_df["return_date"], errors='coerce')
        #     merged_df = merged_df[(df_ret_dates <= pd.to_datetime(filters.Received_Date))]
        
        # Calculate both metrics from the same filtered dataset
        
        if sold == 0:
            return 0
            
        returned = sum_by_key(merged_df, "quantity_returned")
        print("returned:", returned)
        print("sold", sold)
        return (returned / sold) * 100

    def kpi_percentage_change(df, category, col_name, ref_date=None):
        
        # filtered = data[data["Category"] == category].copy()
        filtered = df

        # Convert dates with error handling
        filtered["received_date"] = pd.to_datetime(filtered["Received_Date"], errors='coerce')
        
        # Remove rows with invalid dates
        filtered = filtered.dropna(subset=['received_date'])
        
        # Handle empty dataframe
        if filtered.empty:
            return {
                "today_pct": 0.0,
                "compare_pct": 0.0,
                "pct_change": 0.0,
                "compare_basis": "yesterday" if category == "Fresh Produce" else "month"
            }

        # determine "today"
        if ref_date is None:
            max_date = filtered["received_date"].max()
            if pd.isna(max_date):  # Check if max_date is NaT
                today = pd.Timestamp.now().normalize()
            else:
                today = max_date.normalize()
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
            pct_change = 0.0 if compare_pct == 0 else float("inf")
        else:
            pct_change = (compare_pct - today_pct)

        # return round(today_pct, 2)
        return {
            "today_pct": round(today_pct, 2),
            "compare_pct": round(compare_pct or 0, 2),
            "pct_change": round(pct_change if pct_change != float("inf") else 0.0, 2),
            "compare_basis": "yesterday" if category == "Fresh Produce" else "month"
        }
    
    #aged_pct_by_category
    # def aged_percentage(data, category, ref_date=None):
    #     aged_statuses = ["Expiry Approaching", "Critical - Expiring Soon"]
        
    #     # Handle case where category is None or data is empty
    #     if data.empty or category is None:
    #         return {
    #             "today_pct": 0.0,
    #             "compare_pct": 0.0,
    #             "pct_change": 0.0,
    #             "compare_basis": "yesterday" if category == "Fresh Produce" else "month"
    #         }
        
    #     filtered = data[(data["Category"] == category) &
    #     (data["Inventory_Status"].isin(aged_statuses)) ].copy()

    #     # Convert dates with error handling
    #     filtered["received_date"] = pd.to_datetime(filtered["Received_Date"], errors='coerce')
    #     data["received_date"] = pd.to_datetime(data["Received_Date"], errors='coerce')

    #     # Remove rows with invalid dates
    #     filtered = filtered.dropna(subset=['received_date'])
    #     data = data.dropna(subset=['received_date'])

    #     # Handle case where no valid dates exist after filtering
    #     if filtered.empty or data.empty:
    #         return {
    #             "today_pct": 0.0,
    #             "compare_pct": 0.0,
    #             "pct_change": 0.0,
    #             "compare_basis": "yesterday" if category == "Fresh Produce" else "month"
    #         }

    #     # determine "today"
    #     if ref_date is None:
    #         max_date = filtered["received_date"].max()
    #         if pd.isna(max_date):  # Check if max_date is NaT
    #             max_date = data["received_date"].max()
    #         if pd.isna(max_date):  # If still NaT, use current date
    #             today = pd.Timestamp.now().normalize()
    #         else:
    #             today = max_date.normalize()
    #     else:
    #         today = pd.to_datetime(ref_date).normalize()

    #     # logic for comparison date
    #     if category == "Fresh Produce":
    #         compare_date = today - pd.Timedelta(days=1)
    #     else:  # Dry Goods & General Merchandise
    #         compare_date = (today - pd.offsets.MonthEnd(1)) #today - pd.DateOffset(months=1)
            
    #     # helper to compute %
    #     def calc_pct(df_1, df_2):
    #         actual_qty = df_1["Actual_Quantity_Received"].sum()
    #         aged_qty = df_2["Actual_Quantity_Received"].sum()
    #         return (aged_qty / actual_qty * 100) if actual_qty > 0 else 0

    #     today_pct = calc_pct(data[data["received_date"] <= today], filtered[filtered["received_date"] <= today])
    #     compare_pct = calc_pct(data[data["received_date"] <= compare_date], filtered[filtered["received_date"] <= compare_date])

    #     # % change (today → compare date)
    #     if today_pct == 0:
    #         pct_change = 0.0 if compare_pct == 0 else float("inf")
    #     else:
    #         pct_change = ((compare_pct - today_pct) / today_pct) * 100

    #     return {
    #         "today_pct": round(today_pct, 2),
    #         "compare_pct": round(compare_pct, 2),
    #         "pct_change": round(pct_change if pct_change != float("inf") else 0.0, 2),
    #         "compare_basis": "yesterday" if category == "Fresh Produce" else "month"
    #     }

    # #aged_pct_by_category
    # def aged_percentage(data, category, ref_date=None):
    #     aged_statuses = ["Expiry Approaching", "Critical - Expiring Soon"]
    #     data = data[(data["Category"] == category)].copy()
    #     data["received_date"] = pd.to_datetime(data["Received_Date"])
    #     filtered = data[(data["Inventory_Status"].isin(aged_statuses)) ].copy()
 
    #     # Determine "today"
    #     if ref_date is None:
    #         today = data["received_date"].max().normalize()
    #     else:
    #         today = pd.to_datetime(ref_date).normalize()
 
    #     # Determine comparison date
    #     if category == "Fresh Produce":
    #         compare_date = today - pd.Timedelta(days=1)
    #     else:  # Dry Goods & General Merchandise
    #         compare_date = today - pd.offsets.MonthEnd(1)
 
    #     # Helper to calculate percentage
    #     def calc_pct(df_1, df_2):
    #         actual_qty = df_1["Actual_Quantity_Received"].sum()
    #         aged_qty = df_2["Actual_Quantity_Received"].sum()
    #         return (aged_qty / actual_qty * 100) if actual_qty > 0 else 0
 
    #     # Calculate today's and comparison percentages
    #     today_pct = calc_pct(data[data["received_date"] <= today],
    #                         filtered[filtered["received_date"] <= today])
    #     compare_pct = calc_pct(data[data["received_date"] <= compare_date],
    #                         filtered[filtered["received_date"] <= compare_date])
 
    #     # Calculate percentage change
    #     if today_pct == 0:
    #         pct_change = None if compare_pct == 0 else float("inf")
    #     else:
    #         pct_change = ((compare_pct - today_pct) / today_pct) * 100
 
    #     return {
    #         "today_pct": round(today_pct, 2),
    #         "compare_pct": round(compare_pct, 2),
    #         "pct_change": round(pct_change, 2) if pct_change is not None else None,
    #         "compare_basis": "yesterday" if category == "Fresh Produce" else "month"
    #     }


    def aged_percentage(data, category, ref_date=None):
        aged_statuses = ["Expiry Approaching", "Critical - Expiring Soon"]
        data = data[(data["Category"] == category)].copy()
        data["received_date"] = pd.to_datetime(data["Received_Date"])
        filtered = data[(data["Inventory_Status"].isin(aged_statuses))].copy()

        # Determine "today"
        if ref_date is None:
            max_date = data["received_date"].max()
            # Check if max_date is a valid date (not NaT)
            if pd.isnull(max_date):
                # Handle the case where there are no valid dates.
                # You can set a default date (e.g., today's date) or return a default value.
                # Returning a default value of all zeros might be appropriate if there's no data.
                return {
                    "today_pct": 0,
                    "compare_pct": 0,
                    "pct_change": 0,
                    "compare_basis": "yesterday" if category == "Fresh Produce" else "month"
                }
            else:
                today = max_date.normalize()
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
            pct_change = (compare_pct - today_pct)
        # return today_pct
        return {
            "today_pct": round(today_pct, 2),
            "compare_pct": round(compare_pct, 2),
            "pct_change": round(pct_change, 2) if pct_change is not None else None,
            "compare_basis": "yesterday" if category == "Fresh Produce" else "month"
        }
    #  This is old logic (currentely we are not using these)
    # def shrinkage_pct(df):
    #     actual_qty = sum_by_key(df, "Actual_Quantity_Received")
    #     dump_units = sum_by_key(df, "Number_Dump_Units")
    #     damaged_units = sum_by_key(df, "Number_Damaged_Units")
    #     expired_units = sum_by_key(df, "Number_Expired_Units")

    #     total_shrinkage_units = dump_units + damaged_units + expired_units
    #     print(shrinkage_pct)
    #     return (total_shrinkage_units / actual_qty * 100) if actual_qty else 0

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
        "aged_percentage": aged_percentage(filtered_df, filters.Category),
        "filters_applied": {
            "Category": filters.Category or "All",
            "Sub_Category": filters.Sub_Category or "All",
            "Region": filters.Region_Historical or "All",
            "Store_IDs": filters.Store_ID or "All", 
            "Received_Date": str(filters.Received_Date) if filters.Received_Date else "All",
            "Store_Channel": filters.Store_Channel or "All"
        }          
    }