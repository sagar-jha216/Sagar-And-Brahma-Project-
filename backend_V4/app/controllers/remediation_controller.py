from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.inventory import Inventory
from app.models.remediation_recommendations import RemediationRecommendation
from app.models.stores import Store
from app.models.ngo_partners import NGOPartner
from app.models.liquidation_partners import LiquidationPartner
from typing import Optional, Dict, List
from datetime import date
import pandas as pd
import numpy as np
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points on Earth using Haversine formula"""
    R = 3959  # Radius of Earth in miles
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    dlon, dlat = lon2_rad - lon1_rad, lat2_rad - lat1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def normalize(series, invert=False):
    """Normalize a pandas series to 0-1 range"""
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        return pd.Series([1]*len(series))
    if invert:
        return (max_val - series) / (max_val - min_val)
    else:
        return (series - min_val) / (max_val - min_val)

def find_best_reallocation_store(store_id, sku_sell_through, stores_df):
    """Find the best store for reallocation based on multiple factors"""
    candidate_stores = stores_df[stores_df["Store_ID"] != store_id].copy()
    if candidate_stores.empty:
        return None
    
    store_row = stores_df[stores_df["Store_ID"] == store_id].iloc[0]
    candidate_stores["Distance"] = candidate_stores.apply(
        lambda x: np.sqrt((x["Latitude"] - store_row["Latitude"])**2 + 
                         (x["Longitude"] - store_row["Longitude"])**2), axis=1)
    
    candidate_stores["Sell-through"] = sku_sell_through
    candidate_stores["Inventory"] = candidate_stores["Current_Capacity"]
    candidate_stores["DOS"] = candidate_stores["Current_Capacity"] / (sku_sell_through if sku_sell_through > 0 else 1)
    candidate_stores["Markdown %"] = 0.1
    
    weights = {"Sell-through": 0.4, "Inventory": 0.25, "Distance": 0.2, "DOS": 0.1, "Markdown %": 0.05}
    
    candidate_stores["Sell-through_norm"] = normalize(candidate_stores["Sell-through"])
    candidate_stores["Inventory_norm"] = normalize(candidate_stores["Inventory"], invert=True)
    candidate_stores["Distance_norm"] = normalize(candidate_stores["Distance"], invert=True)
    candidate_stores["DOS_norm"] = normalize(candidate_stores["DOS"], invert=True)
    candidate_stores["Markdown_norm"] = normalize(candidate_stores["Markdown %"], invert=True)
    
    score = (
        candidate_stores["Sell-through_norm"] * weights["Sell-through"] +
        candidate_stores["Inventory_norm"] * weights["Inventory"] +
        candidate_stores["Distance_norm"] * weights["Distance"] +
        candidate_stores["DOS_norm"] * weights["DOS"] +
        candidate_stores["Markdown_norm"] * weights["Markdown %"]
    )
    candidate_stores["Total_Score"] = score
    best_store = candidate_stores.sort_values("Total_Score", ascending=False).head(1)
    return best_store.iloc[0]["Store_ID"] if not best_store.empty else None

def apply_remediation_filters(df_inventory, df_recommendations, filters):
    """Apply filters to inventory and recommendation dataframes"""
    df_inv_filtered = df_inventory.copy()
    df_rec_filtered = df_recommendations.copy()
    
    if filters.Region_Historical:
        df_inv_filtered = df_inv_filtered[df_inv_filtered["Region_Historical"] == filters.Region_Historical]
        filtered_sku_ids = df_inv_filtered["SKU_ID"].unique()
        df_rec_filtered = df_rec_filtered[df_rec_filtered["sku_id"].isin(filtered_sku_ids)]
    
    if filters.Store_ID:
        df_inv_filtered = df_inv_filtered[df_inv_filtered["Store_ID"].isin(filters.Store_ID)]
        df_rec_filtered = df_rec_filtered[df_rec_filtered["store_id"].isin(filters.Store_ID)]
    
    if filters.Store_Channel:
        df_inv_filtered = df_inv_filtered[df_inv_filtered["Store_Channel"].isin(filters.Store_Channel)]
        filtered_sku_ids = df_inv_filtered["SKU_ID"].unique()
        df_rec_filtered = df_rec_filtered[df_rec_filtered["sku_id"].isin(filtered_sku_ids)]
    
    if filters.Category:
        df_inv_filtered = df_inv_filtered[df_inv_filtered["Category"] == filters.Category]
        filtered_sku_ids = df_inv_filtered["SKU_ID"].unique()
        df_rec_filtered = df_rec_filtered[df_rec_filtered["sku_id"].isin(filtered_sku_ids)]
    
    return df_inv_filtered, df_rec_filtered

def get_remediation_recommendations(filters, db: Session):
    """Get remediation recommendations grouped by issue_id"""
    
    # Query all necessary data
    inventory_records = db.query(Inventory).all()
    recommendation_records = db.query(RemediationRecommendation).all()
    store_records = db.query(Store).all()
    
    # Convert to DataFrames
    df_inventory = pd.DataFrame([r.__dict__ for r in inventory_records])
    df_recommendations = pd.DataFrame([r.__dict__ for r in recommendation_records])
    df_stores = pd.DataFrame([r.__dict__ for r in store_records])
    
    # Remove SQLAlchemy internal state columns
    for df in [df_inventory, df_recommendations, df_stores]:
        if '_sa_instance_state' in df.columns:
            df.pop('_sa_instance_state')
    
    # Apply filters
    df_inv_filtered, df_rec_filtered = apply_remediation_filters(df_inventory, df_recommendations, filters)
    
    if df_rec_filtered.empty:
        return {"issues": []}
    
    # Group recommendations by issue_id
    issues = []
    issue_groups = df_rec_filtered.groupby('issue_id')
    
    for issue_id, group in issue_groups:
        if pd.isna(issue_id):  # Skip null issue_ids
            continue
            
        # Get the first record for issue-level information
        first_rec = group.iloc[0]
        
        # Calculate potential loss mitigation (sum of all recommendations for this issue)
        potential_loss_mitigation = group['net_loss_mitigation'].fillna(0).sum()
        
        # Prepare remediation recommendations sorted by rank
        remediations = []
        for _, rec in group.iterrows():
            # Get store name if available
            store_name = None
            if rec['target_name'] and rec['target_name'] in df_stores['Store_ID'].values:
                store_row = df_stores[df_stores['Store_ID'] == rec['target_name']]
                if not store_row.empty:
                    store_name = store_row.iloc[0]['Store_Name']
            
            remediations.append({
                "recommendation_rank": int(rec['recommendation_rank']) if pd.notna(rec['recommendation_rank']) else 1,
                "recommended_action": rec['recommended_action'],
                "action_quantity": int(rec['action_quantity']) if pd.notna(rec['action_quantity']) else 0,
                "target_name": rec['target_name'],
                "target_store_name": store_name,
                "gross_margin_pct": round(rec['gross_margin_pct'], 2) if pd.notna(rec['gross_margin_pct']) else 0,
                "net_loss_mitigation": round(rec['net_loss_mitigation'], 2) if pd.notna(rec['net_loss_mitigation']) else 0,
                "expected_recovery": round(rec['expected_recovery'], 2) if pd.notna(rec['expected_recovery']) else 0,
                "tax_benefit_amount": round(rec['tax_benefit_amount'], 2) if pd.notna(rec['tax_benefit_amount']) else 0
            })
        
        # Sort remediations by recommendation rank
        remediations.sort(key=lambda x: x['recommendation_rank'])
        
        # Determine issue type based on risk level or other criteria
        issue_type = "Lower Sell-Through Rate"  # Default
        if first_rec['risk_level'] == "CRITICAL":
            issue_type = "Critical Expiry"
        elif first_rec['risk_level'] == "VERY_HIGH":
            issue_type = "High Risk Inventory"
        elif first_rec['inventory_age_days'] > 60:
            issue_type = "Seasonal Overstock"
        
        # Get store name for the issue
        issue_store_name = None
        if first_rec['store_id'] in df_stores['Store_ID'].values:
            store_row = df_stores[df_stores['Store_ID'] == first_rec['store_id']]
            if not store_row.empty:
                issue_store_name = store_row.iloc[0]['Store_Name']
        
        issue_data = {
            "issue_id": issue_id,
            "issue_type": issue_type,
            "sku_id": first_rec['sku_id'],
            "product_name": first_rec['product_name'],
            "store_id": first_rec['store_id'],
            "store_name": issue_store_name,
            "quantity_on_hand": int(first_rec['quantity_on_hand']) if pd.notna(first_rec['quantity_on_hand']) else 0,
            "shelf_life_remaining": int(first_rec['shelf_life_remaining']) if pd.notna(first_rec['shelf_life_remaining']) else 0,
            "sell_through_rate_per_day": round(first_rec['Sell_Through_Rate_Per_Day'], 2) if pd.notna(first_rec['Sell_Through_Rate_Per_Day']) else 0,
            "unit_cost": round(first_rec['unit_cost'], 2) if pd.notna(first_rec['unit_cost']) else 0,
            "risk_level": first_rec['risk_level'],
            "category": first_rec['category'],
            "potential_loss_mitigation": round(potential_loss_mitigation, 2),
            "remediations": remediations
        }
        
        issues.append(issue_data)
    
    # Sort issues by potential loss mitigation (highest first)
    issues.sort(key=lambda x: x['potential_loss_mitigation'], reverse=True)
    
    return {
        "issues": issues,
        "total_issues": len(issues),
        "filters_applied": {
            "Region": filters.Region_Historical or "All",
            "Store_IDs": filters.Store_ID or "All",
            "Store_Channel": filters.Store_Channel or "All",
            "Category": filters.Category or "All"
        }
    }