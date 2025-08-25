from sqlalchemy.orm import Session
from sqlalchemy import func, case, desc
from app.models.inventory import Inventory
from app.models.returns import Return
from app.models.stores import Store
# from app.utils.dashboard_filters import apply_inventory_filters
from typing import Optional, Dict
from datetime import date
import pandas as pd


def apply_filters_Inv(df, filters):
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
    return df_filtered

def apply_filters_Return(df, filters):
    df_filtered = df.copy()
    if filters.Category:
        df_filtered = df_filtered[df_filtered["category"] == filters.Category]
    if filters.Store_ID:
        df_filtered = df_filtered[df_filtered["store_id"].isin(filters.Store_ID)]
    return df_filtered


def get_dashboard(filters, db: Session):

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
    filtered_inve = apply_filters_Inv(df_inve, filters)
    filtered_returns = apply_filters_Return(df_returns, filters)


    #Kpis Function
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







    def sum_column(df, col):
        return df[col].fillna(0).sum()
    
    def waste_pct_of_net_sales(df):
        waste_value = ((df["Number_Dump_Units"].fillna(0) + df["Number_Damaged_Units"].fillna(0) + df["Number_Expired_Units"].fillna(0)) * df["Selling_Price_SP"].fillna(0)).sum()
        net_sales = (df["Actual_Quantity_Received"].fillna(0) * df["Selling_Price_SP"].fillna(0)).sum()
        return waste_value / net_sales if net_sales else 0

    def non_sellable_inv(df):

        print(len(df))
        dump_units = sum_column(df, "Number_Dump_Units")
        damaged_units = sum_column(df, "Number_Damaged_Units")
        expired_units = sum_column(df, "Number_Expired_Units")

        Total_non_sellable_units = dump_units + damaged_units + expired_units

        dump_pct = (dump_units / Total_non_sellable_units) * 100 if Total_non_sellable_units else 0
        damage_pct = (damaged_units / Total_non_sellable_units) * 100 if Total_non_sellable_units else 0
        expired_pct = (expired_units / Total_non_sellable_units) * 100 if Total_non_sellable_units else 0

        return dump_pct + damage_pct + expired_pct


    def wastage_by_month_cat(df: pd.DataFrame) -> pd.DataFrame:
        # Ensure date column is in datetime format
        df["Received_Date"] = pd.to_datetime(df["Received_Date"], errors="coerce")

        # Drop rows with invalid dates
        df = df.dropna(subset=["Received_Date"])

        # Extract month as string (e.g., '2025-08')
        df["Month"] = df["Received_Date"].dt.to_period("M").astype(str)

        # Fill missing values to avoid calculation errors
        df.fillna(0, inplace=True)

        # Calculate total waste units
        df["Total_Waste_Units"] = (
            df["Number_Dump_Units"] +
            df["Number_Damaged_Units"] +
            df["Number_Expired_Units"]
        )

        # Calculate waste cost using Selling_Price_SP
        df["Waste_Cost"] = df["Total_Waste_Units"] * df["Selling_Price_SP"]

        # Calculate Net Sales
        df["Net_Sales"] = df["Unit_Sold"] * df["Selling_Price_SP"]

        # Calculate Net Salvage Cost (assuming markdown applies to damaged units)
        df["Net_Salvage_Cost"] = df["Number_Damaged_Units"] * df["Selling_Price_SP"] * (1 - df["Markdown_Pct"])

        # Calculate Shrink Cost (based on missing inventory)
        df["Shrink_Cost"] = df["Difference_System_Actual"] * df["Cost_Price_CP"]

        # Group by Month and Category
        monthly_metrics = df.groupby(["Month", "Category"]).agg({
            "Net_Sales": "sum",
            "Waste_Cost": "sum",
            "Net_Salvage_Cost": "sum",
            "Shrink_Cost": "sum"
        }).reset_index()

        # Rename columns for clarity
        monthly_metrics.columns = [
            "Month", "Category",
            "Total_Net_Sales",
            "Total_Waste_Cost",
            "Total_Salvage_Cost",
            "Total_Shrink_Cost"
        ]

        return monthly_metrics



    def shrink_inv_ratio(df_filtered, df_total):
        shrink_val_cat = sum_column(df_filtered, "Number_Dump_Units") + sum_column(df_filtered, "Number_Damaged_Units") + sum_column(df_filtered, "Number_Expired_Units")
        total_shrink_val = sum_column(df_total, "Number_Dump_Units") + sum_column(df_total, "Number_Damaged_Units") + sum_column(df_total, "Number_Expired_Units")
        cat_units = sum_column(df_filtered, "Actual_Quantity_Received")
        total_inv = sum_column(df_total, "Actual_Quantity_Received")
        shrinkage_value_pct = (shrink_val_cat / total_shrink_val) * 100 if total_shrink_val else 0
        inv_pct = (cat_units / total_inv) * 100 if total_inv else 0
        return shrinkage_value_pct / inv_pct if inv_pct else 0


    def suppliers_highest_shrinkage(data: pd.DataFrame) -> pd.DataFrame:
        
        data["shrink_value"] = (
            data["Number_Damaged_Units"].fillna(0) +
            data["Number_Dump_Units"].fillna(0) +
            data["Number_Expired_Units"].fillna(0)
        ) * data["Selling_Price_SP"].fillna(0)

        data["Total_Inv_value"] = (
            data["Actual_Quantity_Received"].fillna(0) *
            data["Selling_Price_SP"].fillna(0)
        )

        # Group by supplier and calculate shrinkage percentage
        shrink_value_sum = data.groupby("Supplier_Name")["shrink_value"].sum()
        total_inv_value_sum = data.groupby("Supplier_Name")["Total_Inv_value"].sum()

        shrink_pct = (shrink_value_sum / total_inv_value_sum) * 100

        # Format result
        top_10_suppliers = shrink_pct.reset_index(name="Shrinkage_pct") \
                                    .sort_values(by="Shrinkage_pct", ascending=False) \
                                    .head(10)

        return top_10_suppliers


    def top_10_skus_by_shrinkage(data: pd.DataFrame) -> pd.DataFrame:  
        data["shrink_value"] = (
            data["Number_Damaged_Units"].fillna(0) +
            data["Number_Dump_Units"].fillna(0) +
            data["Number_Expired_Units"].fillna(0)
        ) * data["Selling_Price_SP"].fillna(0)

        # Calculate total sales value per SKU
        data["Total_Sales_Value"] = (
            data["Actual_Quantity_Received"].fillna(0) *
            data["Selling_Price_SP"].fillna(0)
        )

        # Group by SKU and compute shrinkage %
        shrink_value_sum = data.groupby("SKU_ID")["shrink_value"].sum()
        sales_value_sum = data.groupby("SKU_ID")["Total_Sales_Value"].sum()

        shrink_pct = (shrink_value_sum / sales_value_sum) * 100

        # Format result
        top_10_skus = shrink_pct.reset_index(name="Shrinkage_pct") \
                                .sort_values(by="Shrinkage_pct", ascending=False) \
                                .head(10)

        return top_10_skus
    
    def Sales_Shrinkage_Salvage(df, returnsDf, df_inve):

            inventory_acc = inventory_accuracy(df)
            damage_percentage = damaged_pct(df)
            dump_percentage = dump_pct(df)
            expired_percentage = expired_pct(df)
            aged_percentage = aged_pct(df)
            shrink_percentage = shrinkage_pct(df)
            return_percentage = return_pct(df, returnsDf)
            
            waste_percentage = waste_pct_of_net_sales(df)
            non_sellable = non_sellable_inv(df)
            shrink_inv = shrink_inv_ratio(df, df_inve)

            swhs = top_10_skus_by_shrinkage(df).to_dict(orient='records')
            su_hs = suppliers_highest_shrinkage(df).to_dict(orient='records')
            monthly_wastage = wastage_by_month_cat(df).to_dict(orient='records')

            return {
                "Inventory_Accuracy": inventory_acc,
                "Damage_%": damage_percentage,
                "Dump_%": dump_percentage,
                "Expired_%": expired_percentage,
                "Aged_%": aged_percentage,
                "Return_%": return_percentage,
                "Shrinkage_%": shrink_percentage,
                "Waste_%_of_Net_Sales": round(waste_percentage, 2),
                "Non_Sellable_Units_%": round(non_sellable, 2),
                "Shrink_to_Inventory_Ratio": round(shrink_inv, 2),
                "Top_SKUs_By_Shrinkage": swhs,
                "Top_Suppliers_By_Shrinkage": su_hs,
                "Monthly_Waste_Cost_By_Category": monthly_wastage
            }



    return {
        "Waste_%_of_Net_Sales": float(round(waste_pct_of_net_sales(filtered_inve), 2)),
        "Non_Sellable_Units": int(round(non_sellable_inv(filtered_inve), 2)),
        "Shrink_to_Inventory_Ratio": float(round(shrink_inv_ratio(filtered_inve, df_inve), 2)),
        "wastage_by_month_cat": wastage_by_month_cat(filtered_inve).to_dict(orient="records"),
        "Top_Suppliers_By_Shrinkage": suppliers_highest_shrinkage(filtered_inve).to_dict(orient="records"),
        "Top_SKUs_By_Shrinkage": top_10_skus_by_shrinkage(filtered_inve).to_dict(orient="records"),
        "Sales_Shrinkage_Salvage": Sales_Shrinkage_Salvage(filtered_inve,df_returns,df_inve),
    }

