from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.inventory import Inventory
from app.models.returns import Return
from app.models.remediation_recommendations import RemediationRecommendation
from app.models.stores import Store
from typing import Optional, Dict, List
from datetime import date
import pandas as pd

def apply_command_center_filters(df_inventory, df_recommendations, filters):
    """Apply filters to both inventory and recommendation dataframes"""
    df_inv_filtered = df_inventory.copy()
    df_rec_filtered = df_recommendations.copy()
    
    # Apply inventory filters
    if filters.Region_Historical:
        df_inv_filtered = df_inv_filtered[df_inv_filtered["Region_Historical"] == filters.Region_Historical]
        # Filter recommendations based on filtered inventory
        filtered_sku_ids = df_inv_filtered["SKU_ID"].unique()
        df_rec_filtered = df_rec_filtered[df_rec_filtered["sku_id"].isin(filtered_sku_ids)]
    
    if filters.Store_ID:
        df_inv_filtered = df_inv_filtered[df_inv_filtered["Store_ID"].isin(filters.Store_ID)]
        df_rec_filtered = df_rec_filtered[df_rec_filtered["store_id"].isin(filters.Store_ID)]
    
    if filters.Store_Channel:
        df_inv_filtered = df_inv_filtered[df_inv_filtered["Store_Channel"].isin(filters.Store_Channel)]
        # Filter recommendations based on filtered inventory
        filtered_sku_ids = df_inv_filtered["SKU_ID"].unique()
        df_rec_filtered = df_rec_filtered[df_rec_filtered["sku_id"].isin(filtered_sku_ids)]
    
    if filters.Received_Date:
        df_inv_filtered = df_inv_filtered[pd.to_datetime(df_inv_filtered["Received_Date"]).dt.date == filters.Received_Date]
        # Filter recommendations based on filtered inventory
        filtered_sku_ids = df_inv_filtered["SKU_ID"].unique()
        df_rec_filtered = df_rec_filtered[df_rec_filtered["sku_id"].isin(filtered_sku_ids)]
    
    return df_inv_filtered, df_rec_filtered

def get_command_center_kpis(filters, db: Session):
    """Generate Command Center KPIs based on shrinkage and return analysis"""
    
    # Query all data with store names
    inventory_records = db.query(Inventory).all()
    recommendation_records = db.query(RemediationRecommendation).all()
    return_records = db.query(Return).all()
    store_records = db.query(Store).all()
    
    # Convert to DataFrames
    df_inventory = pd.DataFrame([r.__dict__ for r in inventory_records])
    df_recommendations = pd.DataFrame([r.__dict__ for r in recommendation_records])
    df_returns = pd.DataFrame([r.__dict__ for r in return_records])
    df_stores = pd.DataFrame([r.__dict__ for r in store_records])
    
    # Remove SQLAlchemy internal state columns
    for df in [df_inventory, df_recommendations, df_returns, df_stores]:
        if '_sa_instance_state' in df.columns:
            df.pop('_sa_instance_state')
    
    # Apply filters
    df_inv_filtered, df_rec_filtered = apply_command_center_filters(df_inventory, df_recommendations, filters)
    
    # --- SHRINKAGE ANALYSIS ---
    
    # Remove duplicates for all risk levels by store_id + sku_id + cogs
    df_rec_dedup = df_rec_filtered.copy()
    df_rec_dedup = df_rec_dedup[~df_rec_dedup.duplicated(subset=["store_id", "sku_id", "cogs"], keep='first')]
    
    # Top 3 stores by shrinkage (total COGS)
    top3_stores_shrinkage = (
        df_rec_dedup.groupby('store_id', as_index=False)
        .agg({'cogs': 'sum'})
        .sort_values('cogs', ascending=False)
        .head(3)
    )
    
    # Add store names by merging with stores data
    top3_stores_shrinkage = top3_stores_shrinkage.merge(
        df_stores[['Store_ID', 'Store_Name', 'Latitude', 'Longitude']], 
        left_on='store_id', 
        right_on='Store_ID', 
        how='left'
    )[['Store_Name', 'cogs', 'Latitude', 'Longitude']].rename(columns={'cogs': 'Total_Shrinkage_Cost'})
    
    # Shrinkage KPIs (excluding LOW risk level)
    shrinkage_filtered = df_rec_dedup[df_rec_dedup['risk_level'] != 'LOW']
    total_shrinkage = shrinkage_filtered['cogs'].fillna(0).sum()
    total_sales = shrinkage_filtered['original_revenue'].fillna(0).sum()
    shrink_perc_of_sales = ((total_sales - total_shrinkage) / total_sales * 100) if total_sales > 0 else 0
    
    shrinkage_kpis = {
        "Total_Known_Shrinkage": round(total_shrinkage, 2),
        #"Total_Known_Sales": round(total_sales, 2),
        "Shrink_Percent_of_Sales": round(shrink_perc_of_sales, 2)
    }
    
    # --- RETURN ANALYSIS ---
    
    # Calculate return inventory value
    df_returns['return_inventory_value'] = df_returns['quantity_returned'].fillna(0) * df_returns['Cost_Price_CP'].fillna(0)
    
    # Top 3 return reasons by inventory value (no category filter)
    top3_return_reasons = (
        df_returns.groupby('return_reason', as_index=False)
        .agg({'return_inventory_value': 'sum'})
        .sort_values('return_inventory_value', ascending=False)
        .head(3)
        .rename(columns={'return_reason': 'Return_Reason', 'return_inventory_value': 'Total_Return_Value'})
    )
    
    # --- ADDITIONAL KPIS ---
    
    # Total items at risk (excluding LOW risk)
    items_at_risk = len(shrinkage_filtered)
    
    # Average days to expiry for critical items
    critical_items = df_rec_dedup[df_rec_dedup['risk_level'].isin(['HIGH', 'VERY_HIGH'])]
    avg_days_to_expiry = critical_items['shelf_life_remaining'].fillna(0).mean() if len(critical_items) > 0 else 0
    
    # Top risk level distribution
    risk_distribution = df_rec_dedup['risk_level'].value_counts().to_dict()
    
    return {
        #"summary": {
        #    "total_items_analyzed": len(df_rec_dedup),
        #    "items_at_risk": items_at_risk,
        #    "avg_days_to_expiry_critical": round(avg_days_to_expiry, 1)
        #},
        "shrinkage_kpis": shrinkage_kpis,
        "top_stores_shrinkage": top3_stores_shrinkage.to_dict('records'),
        "top_return_reasons": top3_return_reasons.to_dict('records'),
        #"risk_distribution": risk_distribution,
        "filters_applied": {
            "Region": filters.Region_Historical or "All",
            "Store_IDs": filters.Store_ID or "All", 
            "Store_Channel": filters.Store_Channel or "All",
            "Received_Date": str(filters.Received_Date) if filters.Received_Date else "All"
        }
    }