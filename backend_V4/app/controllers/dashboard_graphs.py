from sqlalchemy.orm import Session
from sqlalchemy import func, case, desc
from app.models.inventory import Inventory
from app.models.remediation_recommendations import RemediationRecommendation
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


def get_dashboard(filters, db:Session):
    # Query all data from inventory and returns
    inve_records = db.query(Inventory).all()
    returns_records = db.query(Return).all()
    returns_recommendation = db.query(RemediationRecommendation).all()

    # Convert to DataFrames
    df_inve = pd.DataFrame([r.__dict__ for r in inve_records])
    df_returns = pd.DataFrame([r.__dict__ for r in returns_records])
    df_recommendation = pd.DataFrame([r.__dict__ for r in returns_recommendation])
    
    df_inve_all = pd.DataFrame([r.__dict__ for r in db.query(Inventory).all()])

    rem_df = pd.DataFrame([r.__dict__ for r in db.query(RemediationRecommendation).all()])
    rem_df = rem_df[rem_df['recommendation_rank']!=1]
    rem_df = rem_df[['sku_id', 'store_id', 'category', 'received_date', 'quantity_on_hand', 'recommended_action', 'net_loss_mitigation']]
    print(rem_df.head(5))

    df_inve_all["Received_Date"] = pd.to_datetime(df_inve_all["Received_Date"], errors="coerce")
    rem_df["received_date"] = pd.to_datetime(rem_df["received_date"], errors="coerce")


    # Merge inventory with recommendations
    df_inv_remed = pd.merge(
        df_inve,
        rem_df,
        left_on=["SKU_ID", "Store_ID", "Category", "Received_Date", "Inventory_On_Hand"],
        right_on=["sku_id", "store_id", "category", "received_date", "quantity_on_hand"],
        how="inner",
        indicator=True
    )

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
        filtered=df   
        total_waste_value = ((filtered["Number_Dump_Units"]+filtered["Number_Damaged_Units"]+filtered["Number_Expired_Units"])*(filtered["Cost_Price_CP"])).sum()
        
        cogs = (filtered['System_Quantity_Received']*filtered["Cost_Price_CP"]).sum()
        
        if total_waste_value == 0:
            waste_perct_cogs = 0
        else:
            waste_perct_cogs = (total_waste_value/cogs)*100

        return {
            "waste_perct_cogs":round(waste_perct_cogs,2),
            "Total cogs":round(cogs,2),
            "Total Waste" : total_waste_value
        }


    def non_sellable_inv(df):

        print(len(df))
        dump_units = sum_column(df, "Number_Dump_Units")
        damaged_units = sum_column(df, "Number_Damaged_Units")
        expired_units = sum_column(df, "Number_Expired_Units")
        
        Total_non_sellable_units = dump_units + damaged_units + expired_units

        dump_pct = (dump_units / Total_non_sellable_units) * 100 if Total_non_sellable_units else 0
        damage_pct = (damaged_units / Total_non_sellable_units) * 100 if Total_non_sellable_units else 0
        expired_pct = (expired_units / Total_non_sellable_units) * 100 if Total_non_sellable_units else 0
         
 
         
        # Ensure Cost_Price_CP exists
        if "Cost_Price_CP" in df.columns:
            # Create a mask for non-sellable units
            df["Non_Sellable_Units"] = (
                df["Number_Dump_Units"].fillna(0) +
                df["Number_Damaged_Units"].fillna(0) +
                df["Number_Expired_Units"].fillna(0)
            )

            # Calculate row-wise value
            df["Non_Sellable_Value"] = df["Non_Sellable_Units"] * df["Cost_Price_CP"]

            # Final total value
            total_value = df["Non_Sellable_Value"].sum()
        else:
            total_value = 0
 

        # return dump_pct, damage_pct, expired_pct
        summary = pd.DataFrame([{
            "Total_Non_Sellable_Units": int(Total_non_sellable_units),
            "Dump_Pct": round(dump_pct, 2),
            "Damage_Pct": round(damage_pct, 2),
            "Expired_Pct": round(expired_pct, 2),
            "Total_Non_Sellable_Inventory_Value": round(total_value, 2)
        }])
        return summary

    def sales_vs_shrink_vs_waste_vs_salv(df: pd.DataFrame, df_recommendation: pd.DataFrame | None = None) -> pd.DataFrame:
    
        # --- Copy and clean ---
        filtered = df.copy()
        filtered["Received_Date"] = pd.to_datetime(filtered["Received_Date"], errors="coerce")
        # filtered = filtered.dropna(subset=["Received_Date"])
        filtered["Month"] = filtered["Received_Date"].dt.to_period("M").astype(str)

        # --- Safe fill for missing columns ---
        for col in [
            "Number_Dump_Units", "Number_Damaged_Units", "Number_Expired_Units",
            "Cost_Price_CP", "Selling_Price_SP", "Unit_Sold",
            "Difference_System_Actual", "recommended_action", "net_loss_mitigation"
        ]:
            if col not in filtered.columns:
                filtered[col] = 0
        filtered.fillna(0, inplace=True)

        # --- Core metrics ---
        filtered["Total_Waste_Units"] = (
            filtered["Number_Dump_Units"] +
            filtered["Number_Damaged_Units"] +
            filtered["Number_Expired_Units"]
        )

        filtered["Waste"] = filtered["Total_Waste_Units"] * filtered["Cost_Price_CP"]
        filtered["Sales"] = filtered["Unit_Sold"] * filtered["Selling_Price_SP"]
        filtered["Shrinkage"] = filtered["Difference_System_Actual"] * filtered["Cost_Price_CP"]

        # --- Salvage logic ---
        # filtered["Salvage"] = 0
        filtered["Salvage"] = filtered[filtered["recommended_action"] == 'LIQUIDATE']['net_loss_mitigation']

        # --- Monthly aggregation ---
        monthly_metrics = filtered.groupby("Month", as_index=False).agg({
            "Sales": "sum",
            "Shrinkage": "sum",
            "Waste": "sum",
            "Salvage": "sum"
        })

        # --- Rename columns for clarity ---
        monthly_metrics.columns = ["Month", "Sales", "Shrinkage Cost", "Wastege Cost", "Salvage Cost"]

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
        filtered =data;
        
        filtered['shrink_value'] = filtered["Difference_System_Actual"]*filtered["Cost_Price_CP"]
        filtered["total_inv_value"] = filtered["Unit_Sold"]*filtered["Selling_Price_SP"]
        
        # print(filtered.groupby("Supplier_Name")[["shrink_value", "total_inv_value"]].sum())
        # print(filtered.groupby("SKU_ID")[["shrink_value", "total_inv_value"]].sum())

        # shrink_pct = (filtered.groupby("Supplier_Name")["shrink_value"].sum()/(filtered.groupby("Supplier_Name")["shrink_value"].sum() + filtered.groupby("Supplier_Name")["total_inv_value"].sum()))*100
        shrink_pct = (filtered.groupby("Supplier_Name")["shrink_value"].sum()/(filtered.groupby("Supplier_Name")["total_inv_value"].sum()))*100
        print(shrink_pct,"shrink_pct")
        print(len(shrink_pct),"length")


        top_10_suppliers_with_highest_shrinkage = shrink_pct.reset_index(name="Shrinkage_pct").sort_values(by = 'Shrinkage_pct', ascending=False).head(10)
        print(top_10_suppliers_with_highest_shrinkage,"top_10_suppliers_with_highest_shrinkage")
        return top_10_suppliers_with_highest_shrinkage



    def top_10_skus_by_shrinkage(data: pd.DataFrame) -> pd.DataFrame:  
        filtered =data;
        
        filtered['shrink_value'] = filtered["Difference_System_Actual"]*filtered["Cost_Price_CP"]
        filtered["total_inv_value"] = filtered["Unit_Sold"]*filtered["Selling_Price_SP"]

        # shrink_pct = (filtered.groupby("SKU_ID")["shrink_value"].sum()/(filtered.groupby("SKU_ID")["shrink_value"].sum()+ filtered.groupby("SKU_ID")["total_inv_value"].sum()))*100
        shrink_pct = (filtered.groupby("SKU_ID")["shrink_value"].sum()/(filtered.groupby("SKU_ID")["total_inv_value"].sum()))*100
        
        top_10_SKU_with_highest_shrinkage = shrink_pct.reset_index(name="Shrinkage").sort_values(by = 'Shrinkage', ascending=False).head(10)
        # print(top_10_SKU_with_highest_shrinkage,"top_10_SKU_with_highest_shrinkage")
        
        return top_10_SKU_with_highest_shrinkage 


    
    def Sales_Shrinkage_Salvage(df):
      
        # Filter for LIQUIDATE action
        # filtered = df[df["recommended_action"] == 'LIQUIDATE'].copy()
        filtered = df.copy()

        # Convert date and extract month
        filtered["Received_Date"] = pd.to_datetime(filtered["Received_Date"])
        filtered["Month"] = filtered["Received_Date"].dt.to_period("M").astype(str)
        # Calculate financial metrics
        filtered['Sales'] = filtered["Unit_Sold"] * filtered["Selling_Price_SP"]
        filtered['COGS'] = filtered["System_Quantity_Received"] * filtered["Cost_Price_CP"]
        
        filtered["Shrinkage%"] = (filtered["Difference_System_Actual"]/filtered["Actual_Quantity_Received"])*100
        filtered['Loss_Mititagion'] = filtered[filtered["recommended_action"] == 'LIQUIDATE']['net_loss_mitigation']


        monthly_data = filtered.groupby("Month", as_index=False).agg({"Sales":'sum', 'COGS':'sum', 'Loss_Mititagion': 'sum', 'Shrinkage%':'mean'}).reset_index(drop=True)
        
        monthly_data.columns = ["Month", "Sales", 'COGS', "Loss_Mititagion", "Shrinkage%"]
        monthly_data["Salvage%"] = (monthly_data["Loss_Mititagion"]/monthly_data['COGS'])*100
        


        # Final selection
        final_data = monthly_data[["Month", "Sales", "Shrinkage%", "Salvage%"]]

        # Return as dictionary
        return {
            "Monthly_Sales_Shrinkage_Salvage": final_data.to_dict(orient="records")
        }


    return {
        "Waste_%_of_Net_Sales": waste_pct_of_net_sales(filtered_inve),
        "Non_Sellable_Units": non_sellable_inv(filtered_inve).to_dict(orient="records"),
        "Shrink_to_Inventory_Ratio": float(round(shrink_inv_ratio(filtered_inve, df_inve), 2)),
        "sales_vs_shrink_vs_waste_vs_salv": sales_vs_shrink_vs_waste_vs_salv(filtered_inve, df_recommendation).to_dict(orient="records"),
        "Top_Suppliers_By_Shrinkage": suppliers_highest_shrinkage(filtered_inve).to_dict(orient="records"),
        "Top_SKUs_By_Shrinkage": top_10_skus_by_shrinkage(filtered_inve).to_dict(orient="records"),
        "Monthly_Sales_Shrinkage_Salvage": Sales_Shrinkage_Salvage(df_inv_remed)["Monthly_Sales_Shrinkage_Salvage"] 
    }

