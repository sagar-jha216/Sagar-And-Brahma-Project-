from sqlalchemy.orm import Session
from sqlalchemy import func, desc, text
from app.models.return_remediation import ReturnRemediation
from app.models.returns import Return
from app.models.stores import Store
from app.models.inventory import Inventory
from app.models.ngo_partners import NGOPartner
from app.models.liquidation_partners import LiquidationPartner
from app.database import engine
from typing import Optional, Dict, List
from datetime import date
import pandas as pd
import numpy as np
import re

def apply_return_remediation_filters(df, filters):
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


def get_product_name_from_inventory(sku_id, df_inventory):
    """Get product name from inventory DataFrame based on SKU_ID"""
    if df_inventory.empty or pd.isna(sku_id):
        return sku_id  # Return SKU_ID as fallback
    
    # Look up product name in inventory
    product_row = df_inventory[df_inventory['SKU_ID'] == sku_id]
    if not product_row.empty:
        return product_row.iloc[0]['Product_Name']
    else:
        return sku_id  # Return SKU_ID as fallback if not found


def get_return_issues_with_remediations(filters, db: Session):
    """Get return issues with their remediation options based on the actual logic"""
    
    # Query all data
    inventory_records = db.query(Inventory).all()
    return_records = db.query(Return).all()
    remediation_records = db.query(ReturnRemediation).all()
    store_records = db.query(Store).all()
    ngo_records = db.query(NGOPartner).all()
    lqd_records = db.query(LiquidationPartner).all()
    
    # Convert to DataFrames
    df_inv = pd.DataFrame([r.__dict__ for r in inventory_records])
    df_ret = pd.DataFrame([r.__dict__ for r in return_records])
    df_rem = pd.DataFrame([r.__dict__ for r in remediation_records])
    df_sto = pd.DataFrame([r.__dict__ for r in store_records])
    df_lqd = pd.DataFrame([r.__dict__ for r in lqd_records])
    df_ngo = pd.DataFrame([r.__dict__ for r in ngo_records])

    # Remove SQLAlchemy internal state columns
    for df in [df_inv, df_ret, df_rem, df_sto, df_lqd, df_ngo]:
        if '_sa_instance_state' in df.columns:
            df.pop('_sa_instance_state')
        
    # Apply filters
    df_rem_renamed = df_rem.rename(columns={
        'sku_id': 'SKU_ID',
        'store_id': 'Store_ID',
        # 'category': 'Category',
        'cost_price_cp': 'Cost_Price_CP',
        'selling_price_sp': 'Selling_Price_SP'
    })
    merged_df_inv_rem = pd.merge(df_inv, df_rem_renamed, on=['SKU_ID', 'Store_ID', 'Cost_Price_CP','Selling_Price_SP'], how='left', indicator=True)
    merged_df_inv_rem_filtered = apply_return_remediation_filters(merged_df_inv_rem, filters)
    # Check if issue_id column exists, if not, return empty result
    if merged_df_inv_rem_filtered.empty:
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
    
    # # Check if issue_id column exists
    if 'issue_id' not in merged_df_inv_rem_filtered.columns:
        print("Warning: issue_id column not found. Available columns:", merged_df_inv_rem_filtered.columns.tolist())
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
    
    # Get only items with risk level in ["VERY_HIGH", "HIGH", "MEDIUM"] and have issue_id
    # Based on the logic, issue IDs are only assigned to VERY_HIGH, HIGH, MEDIUM risk items
    df_remediation_with_issues = merged_df_inv_rem_filtered[
        (merged_df_inv_rem_filtered['risk_level'].isin(["VERY_HIGH", "HIGH", "MEDIUM"])) & 
        (merged_df_inv_rem_filtered['issue_id'].notna())
    ].copy()
    
    if df_remediation_with_issues.empty:
        return {
            "total_issues": 0,
            "total_potential_loss_mitigation": 0,
            "issues": [],
            "filters_applied": {
                "Region": filters.Region_Historical or "All",
                "Store_IDs": filters.Store_ID or "All",
                "Store_Channel": filters.Store_Channel or "All", 
                "Received_Date": str(filters.Received_Date) if filters.Received_Date else "All",
            }
        }
    
    # Group by issue_id to create issues
    issues = []
    count = 0
    for issue_id, issue_group in df_remediation_with_issues.groupby('issue_id'):
        # Based on the assign_issue_ids logic, VERY_HIGH items with same SKU and return_value share same issue_id
        # HIGH and MEDIUM items get unique issue IDs
        count += 1
        # Get the first record for issue details
        issue_record = issue_group.iloc[0]
        
        # Get store name
        store_row = df_sto[df_sto['Store_ID'] == issue_record['Store_ID']]
        store_name = store_row.iloc[0]['Store_Name'] if not store_row.empty else issue_record['Store_ID']
        
        # Get actual product name from inventory
        product_name = get_product_name_from_inventory(issue_record['SKU_ID'], df_inv)
        
        # Create remediation options for this issue - each row is a separate remediation option
        remediations = []
        total_potential_loss_mitigation = 0
        
        for idx, remediation in issue_group.iterrows():
            # Get target name details - use the target_name directly from the model
            # Set a default value first
            target_display_name = ""  
            prefix = ""
            # Get the prefix once to avoid repeating the split
            if remediation.get('target_name'):
                prefix = remediation['target_name'].split('_')[0]

            # Use an if/elif structure for logical flow
            if prefix == "NGO":
                # 1. Create a boolean mask (the condition)
                mask = (df_ngo['NGO_ID'] == remediation['target_name'])
                
                # 2. Filter the DataFrame to get the resulting Series
                result = df_ngo.loc[mask, 'NGO_Name']
                
                # 3. Check if the result is NOT empty (this is the correct way)
                if not result.empty:
                    # 4. Get the first item from the result
                    target_display_name = result.iloc[0]

            elif prefix == "LQD":
                mask = (df_lqd['Liquidator_ID'] == remediation['target_name'])
                result = df_lqd.loc[mask, 'Liquidator_Name']
                
                if not result.empty:
                    target_display_name = result.iloc[0]
            # Calculate return value: quantity_returned * selling_price_sp
            return_value = (remediation['quantity_returned'] * remediation['Selling_Price_SP']) if remediation['Selling_Price_SP'] else 0
            
            remediation_option = {
                "rank": len(remediations) + 1,
                "recommended_action": remediation['recommended_action'],
                "action_quantity": int(remediation['quantity_returned']) if remediation['quantity_returned'] else 0,
                "target_name": target_display_name,
                "gross_margin_pct": round(remediation['gross_margin_pct'], 2) if remediation['gross_margin_pct'] else 0,
                "gross_margin_amount": round((remediation['gross_margin_pct'] / 100) * return_value, 2) if remediation['gross_margin_pct'] else 0,
                #"expected_recovery": round(remediation['expected_recovery'], 2) if remediation['expected_recovery'] else 0,
                #"tax_benefit_amount": round(remediation['tax_benefit_amount'], 2) if remediation['tax_benefit_amount'] else 0,
                "net_loss_mitigation": round(remediation['net_loss_mitigation'], 2) if remediation['net_loss_mitigation'] else 0
            }
            
            remediations.append(remediation_option)
            total_potential_loss_mitigation += remediation['net_loss_mitigation'] if remediation['net_loss_mitigation'] else 0
        
        # Sort remediations by rank
        remediations.sort(key=lambda x: x['rank'])

        num = re.findall(r'\d+', issue_record['issue_id'])
        
        issue = {
            "issue_id": num[0],
            "product_name": product_name,  # Now using actual Product_Name from inventory
            "store_name": store_name,
            "quantity_returned": int(issue_record['quantity_returned']) if pd.notna(issue_record['quantity_returned']) else 0,
            "return_reason": issue_record['return_reason'],
            "item_condition": issue_record['item_condition'],
            "potential_loss_mitigation": round(total_potential_loss_mitigation, 2),
            "remediations": remediations
        }
        
        issues.append(issue)
    
    # Sort issues by potential loss mitigation (highest first)
    # Based on the assign_issue_ids function, sorting is by return_value, quantity_returned, days_left
    issues.sort(key=lambda x: int(x['issue_id']), reverse=False)
    
    # Add issue ranking
    # for i, issue in enumerate(issues):
    #     issue['issue_id'] = f'ISSUE {i+1}'
    
    return {
        "total_issues": len(issues),
        "issues": issues,
        "filters_applied": {
            "Region": filters.Region_Historical or "All",
            "Store_IDs": filters.Store_ID or "All",
            "Store_Channel": filters.Store_Channel or "All", 
            "Received_Date": str(filters.Received_Date) if filters.Received_Date else "All"
        }
    }


# # def get_single_issue_details(issue_id: str, db: Session):
#     """Get detailed information for a specific issue"""
    
#     # Query remediation records for specific issue
#     try:
#         remediation_records = db.query(ReturnRemediation).filter(
#             ReturnRemediation.issue_id == issue_id
#         ).all()
        
#         print(f"Found {len(remediation_records)} records for issue_id: {issue_id}")
        
#     except Exception as e:
#         print(f"Error querying database for issue_id {issue_id}: {e}")
#         return None
    
#     if not remediation_records:
#         print(f"No records found for issue_id: {issue_id}")
#         return None
    
#     # Convert to DataFrame
#     df_remediation = pd.DataFrame([r.__dict__ for r in remediation_records])
#     if '_sa_instance_state' in df_remediation.columns:
#         df_remediation.pop('_sa_instance_state')
    
#     # Get store data
#     store_records = db.query(Store).all()
#     df_stores = pd.DataFrame([r.__dict__ for r in store_records])
#     if '_sa_instance_state' in df_stores.columns:
#         df_stores.pop('_sa_instance_state')
    
#     # Get inventory data for product name lookup
#     inventory_records = db.query(Inventory).all()
#     df_inventory = pd.DataFrame([r.__dict__ for r in inventory_records])
#     if '_sa_instance_state' in df_inventory.columns:
#         df_inventory.pop('_sa_instance_state')
    
#     # Get issue details from first record
#     issue_record = df_remediation.iloc[0]
    
#     # Get store name
#     store_row = df_stores[df_stores['Store_ID'] == issue_record['store_id']]
#     store_name = store_row.iloc[0]['Store_Name'] if not store_row.empty else issue_record['store_id']
    
#     # Get actual product name from inventory
#     product_name = get_product_name_from_inventory(issue_record['sku_id'], df_inventory)
    
#     # Create remediation options
#     remediations = []
#     total_potential_loss_mitigation = 0
    
#     for idx, remediation in df_remediation.iterrows():
#         # Get target name details - use directly from model
#         target_display_name = remediation['target_name'] if remediation['target_name'] else "N/A"
        
#         # Calculate return value
#         return_value = remediation['quantity_returned'] * remediation['selling_price_sp'] if remediation['selling_price_sp'] else 0
        
#         remediation_option = {
#             "rank": len(remediations) + 1,
#             "recommended_action": remediation['recommended_action'],
#             "action_quantity": int(remediation['quantity_returned']) if remediation['quantity_returned'] else 0,
#             "target_name": target_display_name,
#             "gross_margin_pct": round(remediation['gross_margin_pct'], 2) if remediation['gross_margin_pct'] else 0,
#             "gross_margin_amount": round((remediation['gross_margin_pct'] / 100) * return_value, 2) if remediation['gross_margin_pct'] else 0,
#             #"expected_recovery": round(remediation['expected_recovery'], 2) if remediation['expected_recovery'] else 0,
#             "tax_benefit_amount": round(remediation['tax_benefit_amount'], 2) if remediation['tax_benefit_amount'] else 0,
#             "net_loss_mitigation": round(remediation['net_loss_mitigation'], 2) if remediation['net_loss_mitigation'] else 0
#         }
        
#         remediations.append(remediation_option)
#         total_potential_loss_mitigation += remediation['net_loss_mitigation'] if remediation['net_loss_mitigation'] else 0
    
#     # Sort remediations by rank
#     remediations.sort(key=lambda x: x['rank'])
    
#     return {
#         "issue_id": issue_id,
#         "product_name": product_name,  # Now using actual Product_Name from inventory
#         "store_name": store_name,
#         "quantity_returned": int(issue_record['quantity_returned']) if pd.notna(issue_record['quantity_returned']) else 0,
#         "return_reason": issue_record['return_reason'],
#         "item_condition": issue_record['item_condition'],
#         "potential_loss_mitigation": round(total_potential_loss_mitigation, 2),
#         "remediations": remediations
#     }