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
import re

def apply_remediation_filters(df, filters):
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


def resolve_target_name(target_id, df_stores, df_ngo_partners, df_liquidation_partners):
    """
    Resolve target_name to actual name based on ID type
    Returns the appropriate name and target type
    """
    if pd.isna(target_id) or not target_id:
        return None, None
    
    target_id = str(target_id).strip()
    
    # Check if it's a Store ID (starts with STR_)
    if target_id.startswith('STR_'):
        store_match = df_stores[df_stores['Store_ID'] == target_id]
        if not store_match.empty:
            return store_match.iloc[0]['Store_Name'], 'Store'
    
    # Check if it's an NGO ID (starts with NGO_)
    elif target_id.startswith('NGO_'):
        ngo_match = df_ngo_partners[df_ngo_partners['NGO_ID'] == target_id]
        if not ngo_match.empty:
            return ngo_match.iloc[0]['NGO_Name'], 'NGO'
    
    # Check if it's a Liquidator ID (starts with LIQ_)
    elif target_id.startswith('LIQ_'):
        liquidator_match = df_liquidation_partners[df_liquidation_partners['Liquidator_ID'] == target_id]
        if not liquidator_match.empty:
            return liquidator_match.iloc[0]['Liquidator_Name'], 'Liquidator'
    
    # If no pattern matches, try to find in all tables
    else:
        # Try stores table
        store_match = df_stores[df_stores['Store_ID'] == target_id]
        if not store_match.empty:
            return store_match.iloc[0]['Store_Name'], 'Store'
        
        # Try NGO table
        ngo_match = df_ngo_partners[df_ngo_partners['NGO_ID'] == target_id]
        if not ngo_match.empty:
            return ngo_match.iloc[0]['NGO_Name'], 'NGO'
        
        # Try liquidation partners table
        liquidator_match = df_liquidation_partners[df_liquidation_partners['Liquidator_ID'] == target_id]
        if not liquidator_match.empty:
            return liquidator_match.iloc[0]['Liquidator_Name'], 'Liquidator'
    
    # Return original ID if no match found
    return target_id, 'Unknown'

def get_remediation_recommendations(filters, db: Session):
    """Get remediation recommendations grouped by issue_id"""
    
    # Query all necessary data
    # --- OPTIMIZED QUERIES ---

    # For Inventory: Only columns needed for merging and final issue data
    inventory_records = db.query(
        Inventory.SKU_ID,
        Inventory.Store_ID,
        Inventory.Category,
        Inventory.Received_Date,
        Inventory.Sell_Through_Rate_Per_Day,
        # Inventory.Product_Name,
        Inventory.Inventory_On_Hand,
        Inventory.Shelf_Life_Remaining,
        Inventory.Region_Historical,
        Inventory.Store_Channel
        # Inventory.unit_cost
    ).all()

    # For RemediationRecommendation: Columns for merging, grouping, and constructing the final output
    recommendation_records = db.query(
        RemediationRecommendation.sku_id,
        RemediationRecommendation.product_name,
        RemediationRecommendation.quantity_on_hand,
        RemediationRecommendation.unit_cost,        
        RemediationRecommendation.store_id,
        RemediationRecommendation.shelf_life_remaining,
        RemediationRecommendation.category,
        RemediationRecommendation.received_date,
        RemediationRecommendation.Sell_Through_Rate_Per_Day, # Assuming this name is correct in the model
        RemediationRecommendation.issue_id,
        RemediationRecommendation.net_loss_mitigation,
        RemediationRecommendation.recommendation_rank,
        RemediationRecommendation.recommended_action,
        RemediationRecommendation.action_quantity,
        RemediationRecommendation.target_name,
        RemediationRecommendation.gross_margin_pct,
        RemediationRecommendation.unit_price
    ).all()

    # For Store: Used in filtering, resolving target names, and getting the final issue store name
    store_records = db.query(
        Store.Store_ID,
        Store.Store_Name,
        # Store.Store_Region,
        # Store.Store_Channel
    ).all()

    # For NGOPartner: Only needed for the ID-to-Name lookup
    ngo_records = db.query(
        NGOPartner.NGO_ID,
        NGOPartner.NGO_Name
    ).all()

    # For LiquidationPartner: Only needed for the ID-to-Name lookup
    liquidation_records = db.query(
        LiquidationPartner.Liquidator_ID,
        LiquidationPartner.Liquidator_Name
    ).all()
    
    # Convert to DataFrames
    df_inv = pd.DataFrame([r._asdict() for r in inventory_records])
    df_rec = pd.DataFrame([r._asdict() for r in recommendation_records])
    df_sto = pd.DataFrame([r._asdict() for r in store_records])
    df_ngo = pd.DataFrame([r._asdict() for r in ngo_records])
    df_liq = pd.DataFrame([r._asdict() for r in liquidation_records])
    # Remove SQLAlchemy internal state columns
    # for df in [df_inv, df_rec, df_sto, df_ngo, df_liq]:
    #     if '_sa_instance_state' in df.columns:
    #         df.pop('_sa_instance_state')
    
    df_rec_renamed = df_rec.rename(columns={
        'sku_id': 'SKU_ID',
        'store_id': 'Store_ID',
        'category': 'Category',
        'received_date': 'Received_Date',
    })
    df_rec_renamed['Received_Date'] = pd.to_datetime(df_rec_renamed['Received_Date'])
    merged_df_inv_rec = pd.merge(df_inv, df_rec_renamed, on=['SKU_ID', 'Store_ID', 'Category', 'Received_Date', 'Sell_Through_Rate_Per_Day'], how='left', indicator=True)
    merged_df_inv_rec_filtered = apply_remediation_filters(merged_df_inv_rec, filters)

    if merged_df_inv_rec_filtered.empty:
        return {
                    "total_issues": 0,
                    "total_potential_loss_mitigation": 0,
                    "issues": [],
                    "filters_applied": {
                        "Region": filters.Region_Historical or "All",
                        "Store_IDs": filters.Store_ID or "All",
                        "Store_Channel": filters.Store_Channel or "All", 
                        "Received_Date": str(filters.Received_Date) if filters.Received_Date else "All"
                    }
                }    
    # Group recommendations by issue_id
    issues = []
    issue_groups = merged_df_inv_rec_filtered.groupby('issue_id')
    
    count = 0

    for issue_id, group in issue_groups:
        if pd.isna(issue_id):  # Skip null issue_ids
            continue
            
        count += 1
        # Get the first record for issue-level information
        first_rec = group.iloc[0]
        
        # Calculate potential loss mitigation (highest net_loss_mitigation among all recommendations for this issue)
        potential_loss_mitigation = group['net_loss_mitigation'].fillna(0).max()
        
        # Prepare remediation recommendations sorted by rank
        remediations = []
        for _, rec in group.iterrows():
            # Resolve target_name to actual name
            resolved_name, target_type = resolve_target_name(
                rec['target_name'], 
                df_sto, 
                df_ngo, 
                df_liq
            )
            
            # Determine target_store_name for backward compatibility
            target_store_name = None
            if target_type == 'Store':
                target_store_name = resolved_name
            elif rec['target_name'] and str(rec['target_name']).startswith('STR_'):
                # If it's a store ID but didn't resolve, try to get store name
                store_match = df_sto[df_sto['Store_ID'] == rec['target_name']]
                if not store_match.empty:
                    target_store_name = store_match.iloc[0]['Store_Name']
            
            remediations.append({
                "recommendation_rank": int(rec['recommendation_rank']) if pd.notna(rec['recommendation_rank']) else 1,
                "recommended_action": rec['recommended_action'],
                "action_quantity": int(rec['action_quantity']) if pd.notna(rec['action_quantity']) else 0,
                "target_id": rec['target_name'],  # Original ID for reference
                "target_name": resolved_name,     # Resolved name (NGO_Name, Liquidator_Name, or Store_Name)
                "target_store_name": target_store_name,  # Required field for API compatibility
                "target_type": target_type,       # Type indicator (NGO, Liquidator, Store, Unknown)
                "gross_margin_pct": round(rec['gross_margin_pct'], 2) if pd.notna(rec['gross_margin_pct']) else 0,
                "gross_margin_amount": round((rec['gross_margin_pct'] / 100) * rec['action_quantity'] * rec['unit_price'], 2) if rec['gross_margin_pct'] else 0,
                "net_loss_mitigation": round(rec['net_loss_mitigation'], 2) if pd.notna(rec['net_loss_mitigation']) else 0,
                #"expected_recovery": round(rec['expected_recovery'], 2) if pd.notna(rec['expected_recovery']) else 0,
                #"tax_benefit_amount": round(rec['tax_benefit_amount'], 2) if pd.notna(rec['tax_benefit_amount']) else 0
            })
        
        # Sort remediations by recommendation rank
        #remediations.sort(key=lambda x: x['recommendation_rank'])
        
        # Determine issue type based on risk level or other criteria
        # issue_type = "Lower Sell-Through Rate"  # Default
        # if first_rec['risk_level'] == "CRITICAL":
        #     issue_type = "Critical Expiry"
        # elif first_rec['risk_level'] == "VERY_HIGH":
        #     issue_type = "High Risk Inventory"
        # elif first_rec['inventory_age_days'] > 60:
        #     issue_type = "Seasonal Overstock"
        
        # Get store name for the issue
        issue_store_name = None
        if first_rec['Store_ID'] in df_sto['Store_ID'].values:
            store_row = df_sto[df_sto['Store_ID'] == first_rec['Store_ID']]
            if not store_row.empty:
                issue_store_name = store_row.iloc[0]['Store_Name']
        
        # num = re.findall(r'\d+', first_rec['issue_id'])
        
        issue_data = {
            "issue_id": re.findall(r'\d+', first_rec['issue_id'])[0],
            "product_name": first_rec['product_name'],
            "store_name": issue_store_name,
            "quantity_on_hand": int(first_rec['quantity_on_hand']) if pd.notna(first_rec['quantity_on_hand']) else 0,
            "shelf_life_remaining": int(first_rec['shelf_life_remaining']) if pd.notna(first_rec['shelf_life_remaining']) else 0,
            "sell_through_rate_per_day": round(first_rec['Sell_Through_Rate_Per_Day'], 2) if pd.notna(first_rec['Sell_Through_Rate_Per_Day']) else 0,
            "unit_cost": round(first_rec['unit_cost'], 2) if pd.notna(first_rec['unit_cost']) else 0,
            "potential_loss_mitigation": round(potential_loss_mitigation, 2),
            "remediations": remediations
        }
        
        issues.append(issue_data)
    
    # Sort issues by potential loss mitigation (highest first)
    issues.sort(key=lambda x: int(x['issue_id']), reverse=False)
    
    # for i, issue in enumerate(issues):
    #     issue['issue_id'] = f'ISSUE {i+1}'

    return {
        "total_issues": len(issues),
        "issues": issues,
        "filters_applied": {
            "Region": filters.Region_Historical or "All",
            "Store_IDs": filters.Store_ID or "All",
            "Received_Date": str(filters.Received_Date) if filters.Received_Date else "All",
            "Store_Channel": filters.Store_Channel or "All"
        }
    }