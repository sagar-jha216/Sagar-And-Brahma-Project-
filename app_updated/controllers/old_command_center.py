from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.inventory import Inventory
from app.models.return_remediation import ReturnRemediation
from app.models.remediation_recommendations import RemediationRecommendation
from app.models.stores import Store
from typing import Optional, Dict, List
from datetime import date, datetime
import pandas as pd
import os

def apply_command_center_filters(df, filters):
    """Apply filters to dataframe"""
    df_filtered = df.copy()    
    if filters.Region_Historical:
        df_filtered = df_filtered[df_filtered["Region_Historical"] == filters.Region_Historical]
    if filters.Store_ID:
        df_filtered = df_filtered[df_filtered["Store_ID"].isin(filters.Store_ID)]
    if filters.Store_Channel:
        df_filtered = df_filtered[df_filtered["Store_Channel"].isin(filters.Store_Channel)]
    if filters.Received_Date:
        df_filtered = df_filtered[pd.to_datetime(df_filtered["Received_Date"]).dt.date <= filters.Received_Date]
    return df_filtered

def get_command_center_kpis(filters, db: Session, export_to_excel=False, output_dir="Output_Files"):
    """Generate Command Center KPIs based on shrinkage and return analysis"""
    
    # Query all data with store names
    inventory_records = db.query(Inventory).all()
    recommendation_records = db.query(RemediationRecommendation).all()
    return_records = db.query(ReturnRemediation).all()
    store_records = db.query(Store).all()
    
    # Convert to DataFrames
    df_inv = pd.DataFrame([r.__dict__ for r in inventory_records])
    df_rec = pd.DataFrame([r.__dict__ for r in recommendation_records])
    df_ret = pd.DataFrame([r.__dict__ for r in return_records])
    df_sto = pd.DataFrame([r.__dict__ for r in store_records])
    
    # Remove SQLAlchemy internal state columns
    for df in [df_inv, df_rec, df_ret, df_sto]:
        if '_sa_instance_state' in df.columns:
            df.pop('_sa_instance_state')
    
    df_rec_renamed = df_rec.rename(columns={
        'sku_id': 'SKU_ID',
        'store_id': 'Store_ID',
        'category': 'Category',
        'received_date': 'Received_Date',
    })

    df_ret_renamed = df_ret.rename(columns={
        'sku_id': 'SKU_ID',
        'store_id': 'Store_ID',
        'category': 'Category',
        #'sub_category': 'Sub_Category',
        'cost_price_cp': 'Cost_Price_CP'
    })
    # Apply filters
    df_rec_renamed['Received_Date'] = pd.to_datetime(df_rec_renamed['Received_Date'])
    merged_df_inv_rec = pd.merge(df_inv, df_rec_renamed, on=['SKU_ID', 'Store_ID', 'Category', 'Received_Date', 'Sell_Through_Rate_Per_Day'], how='left', indicator=True)
    merged_df_inv_ret = pd.merge(df_inv, df_ret_renamed, on=['SKU_ID', 'Store_ID', 'Category', 'Cost_Price_CP'], how='left', indicator=True)
    merged_df_inv_rec_filtered = apply_command_center_filters(merged_df_inv_rec, filters)
    merged_df_inv_ret_filtered = apply_command_center_filters(merged_df_inv_ret, filters)
    # df_inv_filtered, df_rec_filtered, df_ret_filtered = apply_command_center_filters(df_inventory, df_recommendations, df_returns, filters)
    
    # --- SHRINKAGE ANALYSIS ---
    
    # UPDATED: Remove duplicates ONLY for VERY_HIGH risk level (aligned with file code)
    df_rec_dedup = merged_df_inv_rec_filtered.copy()
    df_rec_dedup = df_rec_dedup[
        (df_rec_dedup["risk_level"] != "VERY_HIGH") | (df_rec_dedup["net_loss_mitigation"]==df_rec_dedup.groupby(["Store_ID", "SKU_ID", "cogs", "issue_id"])["net_loss_mitigation"].transform("max"))
    ]
    
    df_rec_dedup = df_rec_dedup[df_rec_dedup['risk_level'] != 'LOW']
    df_rec_dedup["sales"] = df_rec_dedup["action_quantity"]*df_rec_dedup["unit_price"]
    #df_rec_dedup["cogs"] = df_rec_dedup["action_quantity"]*df_rec_dedup["unit_cost"]
    
    # Top 3 stores by shrinkage (total COGS)
    top3_stores_shrinkage = (
        df_rec_dedup.groupby('Store_ID', as_index=False)
        .agg({'cogs': 'sum'})
        .sort_values('cogs', ascending=False)
        .head(3)
    )
    
    # Add store names by merging with stores data
    top3_stores_shrinkage = pd.merge(top3_stores_shrinkage, df_sto, on=['Store_ID'], how='left', indicator=True)

    # top3_stores_shrinkage = top3_stores_shrinkage.merge(
    #     df_sto[['Store_ID', 'Store_Name', 'Latitude', 'Longitude','Store_City','Store_State']], 
    #     left_on='Store_ID', 
    #     right_on='Store_ID', 
    #     how='left'
    # )[['Store_ID', 'Store_Name', 'cogs', 'Latitude', 'Longitude','Store_City','Store_State']]

    top3_stores_shrinkage = top3_stores_shrinkage[['Store_ID', 'Store_Name', 'cogs', 'Latitude', 'Longitude','Store_City','Store_State']].rename(columns={'cogs': 'Total_Shrinkage_Cost'})
    # .rename(columns={'cogs': 'Total_Shrinkage_Cost'}
    # Shrinkage KPIs (excluding LOW risk level)
    total_shrinkage = df_rec_dedup['cogs'].fillna(0).sum()
    total_sales = (df_rec_dedup['sales']).fillna(0).sum()
    shrink_perc_of_sales = ((total_sales - total_shrinkage) / total_sales * 100) if total_sales > 0 else 0
    
    # UPDATED: Include Total_Known_Sales (aligned with file code)
    shrinkage_kpis = {
        "Total_Known_Shrinkage": round(total_shrinkage, 2),
        "Total_Known_Sales": round(total_sales, 2),
        "Shrink_Percent_of_Sales": round(shrink_perc_of_sales, 2)
    }
    
    # Top 3 return reasons by inventory value using FILTERED returns data
    top3_return_reasons = (
        merged_df_inv_ret_filtered.groupby('return_reason', as_index=False)
        .agg({'cogs': 'sum'})
        .sort_values('cogs', ascending=False)
        .head(3)
        .rename(columns={'return_reason': 'Return_Reason', 'cogs': 'Total_Return_Value'})
    )
    # 'cogs': 'Total_Return_Value'
    # --- ADDITIONAL KPIS ---
    
    # Total items at risk (excluding LOW risk)
    #items_at_risk = len(shrinkage_filtered)
    
    # Average days to expiry for critical items
    critical_items = df_rec_dedup[df_rec_dedup['risk_level'].isin(['HIGH', 'VERY_HIGH'])]
    avg_days_to_expiry = critical_items['shelf_life_remaining'].fillna(0).mean() if len(critical_items) > 0 else 0
    
    # Top risk level distribution
    risk_distribution = df_rec_dedup['risk_level'].value_counts().to_dict()
    
    # Prepare data for potential Excel export
    kpi_data = {
        "top3_stores": top3_stores_shrinkage,
        "shrinkage_kpis": pd.DataFrame({
            "Metric": ["Total Known Shrinkage", "Total Known Sales", "Shrink % of Sales"],
            "Value": [total_shrinkage, total_sales, shrink_perc_of_sales]
        }),
        "top3_return_reasons": top3_return_reasons
    }
    
    # UPDATED: Optional Excel export (aligned with file code functionality)
    #if export_to_excel:
        #export_kpis_to_excel(kpi_data, output_dir)
    
    return {
        "summary": {
            "total_items_analyzed": len(df_rec_dedup),
            #"items_at_risk": items_at_risk,
            "avg_days_to_expiry_critical": round(avg_days_to_expiry, 1)
        },
        "Total_Shrink_Impact": shrinkage_kpis,
        "Top_3_Stores": top3_stores_shrinkage.to_dict('records'),
        "Top_3_Root_Causes": top3_return_reasons.to_dict('records'),
        "risk_distribution": risk_distribution,
        "filters_applied": {
            "Region": filters.Region_Historical or "All",
            "Store_IDs": filters.Store_ID or "All", 
            "Received_Date": str(filters.Received_Date) if filters.Received_Date else "All",
            "Store_Channel": filters.Store_Channel or "All"
        }
    }

# def export_kpis_to_excel(kpi_data, output_dir="Output_Files"):
#     """Export KPI data to Excel file (aligned with file code functionality)"""
    
#     # Create output directory if it doesn't exist
#     os.makedirs(output_dir, exist_ok=True)
    
#     # Generate timestamped filename
#     now = datetime.now().strftime("%Y%m%d_%H%M%S")
#     output_path = os.path.join(output_dir, f"Shrinkage_and_Return_KPIs_{now}.xlsx")
    
#     try:
#         with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
#             kpi_data["top3_stores"].to_excel(writer, index=False, sheet_name='Top3_Stores_Shrinkage')
#             kpi_data["shrinkage_kpis"].to_excel(writer, index=False, sheet_name='Shrinkage_KPIs')
#             kpi_data["top3_return_reasons"].to_excel(writer, index=False, sheet_name='Top3_Return_Reasons')
        
#         print(f"✅ KPI Report saved to: {output_path}")
#         return output_path
#     except Exception as e:
#         print(f"❌ Error saving KPI Report: {str(e)}")
#         return None