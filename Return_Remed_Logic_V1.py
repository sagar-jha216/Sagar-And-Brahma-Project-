##E-commerce orders returns to the Warehouse not to the stores which fullfill the orders.

#import libraies
import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta


# --- Load the data files ---

shrinksense_file = "Output_Files/" + "ShrinkSense_Complete_System_20250829_171131.xlsx"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Load required sheets
returns_df = pd.read_excel(shrinksense_file, sheet_name='returns')
#stores_df = pd.read_excel(shrinksense_file, sheet_name='stores')
ngo_df = pd.read_excel(shrinksense_file, sheet_name='ngo_partners')
liquidator_df = pd.read_excel(shrinksense_file, sheet_name='liquidation_partners')

#Columns in Final table
#columns = [Returned_Date, SKU_ID, Returned_Quantity, Unit_Cost, Unit_Price, total_shelf_life,shelf_life_left, Return_Reason, Item_Condition]

returns_df['return_value'] = returns_df["quantity_returned"]*returns_df["Cost_Price_CP"]
#Logic-------------------------------------------------------------------------------

#Calclate time risk
def calculate_time_risk(days_to_expiry, total_shelf_life):
    if total_shelf_life == 0: 
        return 0.0
    if days_to_expiry <= 0: 
        return 1.0
    return 1 - (days_to_expiry / total_shelf_life)

#Calculate risk level
def calculate_risk_level(category, days_to_expiry, total_shelf_life):
    risk = calculate_time_risk(days_to_expiry, total_shelf_life)

    if category == "Dry Goods":
        if risk > 0.9:
            return "CRITICAL"
        elif risk > 0.8:
            return "VERY_HIGH"
        elif risk >= 0.6:
            return "HIGH"
        elif risk >= 0.4:
            return "MEDIUM"
        elif risk >= 0.0:
            return "LOW"
    elif category == "General Merchandise":
        if risk >= 0.95:
            return "CRITICAL"
        elif risk >= 0.9:
            return "VERY_HIGH"
        elif risk >= 0.7:
            return "HIGH"
        elif risk >= 0.5:
            return "MEDIUM"
        elif risk >= 0.0:
            return "LOW"
    else:
        return "UNKNOWN_CATEGORY"


def assign_issue_ids(df):
    """
    Assigns issue IDs to rows based on risk_level, COGS, quantity_on_hand, and shelf_life_remaining.
    Only rows with risk_level in ["VERY_HIGH", "HIGH", "MEDIUM"] receive issue IDs.
    VERY_HIGH risk items with same SKU and COGS but different recommended_action will share the same issue ID.

    Parameters:
        df (pd.DataFrame): Input dataframe containing 'risk_level', 'sku_id', 'cogs',
                           'quantity_on_hand', 'shelf_life_remaining', 'recommended_action'

    Returns:
        pd.DataFrame: New dataframe with 'group_key' and 'issue_id' columns added
    """

    # Step 1: Filter by risk level
    df_filtered = df[df["risk_level"].isin(["VERY_HIGH", "HIGH", "MEDIUM"])].copy()
    df_unfiltered = df[~df["risk_level"].isin(["VERY_HIGH", "HIGH", "MEDIUM"])].copy()

    # Step 2: Sort filtered data
    df_filtered.sort_values(
        by=["return_value", "quantity_returned", "days_left"],
        ascending=[False, False, True],
        inplace=True
    )

    # Step 3: Assign group key
    df_filtered["group_key"] = np.where(
        df_filtered["risk_level"] == "VERY_HIGH",
        df_filtered["sku_id"].astype(str) + "_" + df_filtered["return_value"].astype(str),
        df_filtered.index.astype(str)  # Unique key for each row for HIGH/MEDIUM
    )

    # Step 4: Assign ISSUE IDs
    df_filtered["issue_id"] = "ISSUE " + (
        df_filtered.groupby("group_key", sort=False).ngroup() + 1
    ).astype(str)

    # Step 5: For unfiltered, set NaN for group_key and issue_id
    df_unfiltered[["group_key", "issue_id"]] = np.nan

    # Step 6: Combine both parts
    df_final = pd.concat([df_filtered, df_unfiltered], ignore_index=True)

    return df_final
    
#Find best donation centre to donate
def find_best_donation_center(category, quantity):
    eligible_ngos = ngo_df[(ngo_df["Acceptance_Criteria_Met"] == True) & (ngo_df["NGO_Type"].str.contains(category))]
    if eligible_ngos.empty:
        return None
    # Distance and past success are not available in data, so we just use capacity as proxy
    eligible_ngos = eligible_ngos.sort_values("Acceptance_Capacity_Dry_Goods", ascending=False) # Using Dry Goods as a proxy for now
    return eligible_ngos.iloc[0]["NGO_ID"]

#Find best Liquidator to liquidate
def find_best_liquidator(category, quantity):
    eligible_liqs = liquidator_df[(liquidator_df["Offer Price (% of MRP)"] > 0) & (liquidator_df["Liquidator_Type"].str.contains(category))]
    if eligible_liqs.empty:
        return None
    eligible_liqs = eligible_liqs.sort_values("Offer Price (% of MRP)", ascending=False)
    return eligible_liqs.iloc[0]["Liquidator_ID"]


def get_return_action(category, return_reason, item_condition, shelf_life_remaining, risk_level, quantity, unit_price, unit_cost):
    # Immediate disposal rules
    if shelf_life_remaining <= 2 or risk_level == "CRITICAL":
        return "DISPOSE"

    # High severity
    if risk_level == "VERY_HIGH":
        if return_reason == "Packaging Damaged":
            return "DISPOSE"
        else:
            return "DONATE"

    if risk_level == "HIGH":
        if return_reason == "Packaging Damaged":
            return "DISPOSE"
        else:
            return "DONATE"

    # Low/Medium Risk
    if risk_level in ["LOW", "MEDIUM"]:
        if item_condition == "New/Sealed":
            return "RESELL"
        elif item_condition in ["Opened", "Good Condition", "Unused"]:
            return "CLEARANCE"
        elif item_condition in ["Defective", "Expired", "Spoiled"]:
            return "DISPOSE"
        elif return_reason == "Packaging Damaged":
            if category == "Dry Goods":
                return "CLEARANCE"
            elif category == "General Merchandise":
                return "LIQUIDATE"
        else:
            return "LIQUIDATE"

        # Fallback
        return "DISPOSE"

            
        # Suggest two recommendations - Donate & Liquidation
        # Get both donation and liquidation options
        donation_center = find_best_donation_center(category, quantity)
        liquidation_partner = find_best_liquidator(category, quantity)
        if donation_center:
            # First recommendation: DONATE
            action_1 = "DONATE"
            target_name_1 = donation_center

            # Calculate expected recovery for donation
            expected_recovery_1 = 0  # No direct revenue from donation
            ngo_row = ngo_df[ngo_df["NGO_ID"] == donation_center]
            if not ngo_row.empty:
                # Use IRS enhanced deduction formula
                tax_rate = 0.21  # Or your configured corporate tax rate

                # Calculate estimated tax savings by applying tax rate
                tax_benefit_amount_1 = unit_cost * tax_rate * quantity
            else:
                tax_benefit_amount_1 = 0
       
            net_loss_mitigation_1 = max(0, (quantity * unit_price - expected_recovery_1 - tax_benefit_amount_1))

        if liquidation_partner:    
            # Second recommendation: LIQUIDATE
            action_2 = "LIQUIDATE"
            target_name_2 = liquidation_partner
            
            # Calculate expected recovery for liquidation
            liquidator_row = liquidator_df[liquidator_df["Liquidator_ID"] == liquidation_partner]
            if not liquidator_row.empty:
                recovery_rate = liquidator_row.iloc[0]["Offer Price (% of MRP)"] / 100 # Using \'Offer Price (% of MRP)\' as recovery rate
                expected_recovery_2 = quantity * unit_price * recovery_rate
            else:
                expected_recovery_2 = quantity * unit_cost
            
            tax_benefit_amount_2 = 0  # No tax benefit for liquidation
            net_loss_mitigation_2 = max(0, (quantity * unit_price - expected_recovery_2))
        
        # If both donation center and liquidation partner are not available
        if not donation_center and not liquidation_partner:
            return "DISPOSE"
        
        # If only donation center is available
        elif donation_center and not liquidation_partner:
            return "DONATE"

        # If only liquidation partner is available
        elif liquidation_partner and not donation_center:
            return "LIQUIDATE"
        
        elif net_loss_mitigation_1 > net_loss_mitigation_2:
            return "DONATE"
        else:
            return "LIQUIDATE"
        
        
output_records = []

for idx, return_item in returns_df.iterrows():
    category = return_item['category']
    return_reason = return_item['return_reason']
    days_left = return_item['days_left']
    quantity = return_item['quantity_returned']
    store_id = return_item['store_id']     
    unit_price = return_item["Selling_Price_SP"] 
    unit_cost = return_item["Cost_Price_CP"]
    total_shelf_life = return_item["shelf_life"]
    item_condition = return_item["item_condition"]
    return_value = return_item["return_value"]


    risk_level =  calculate_risk_level(category, days_left, total_shelf_life)
    action = get_return_action (category, return_reason, item_condition, days_left, risk_level,quantity,unit_price,unit_cost )

    # Calculate expected recovery 
    target_name = None
    if action == "DISPOSE":
        expected_recovery = 0
    elif action == "DONATE":
        target_name = find_best_donation_center(category, quantity)
        expected_recovery = 0
    elif action == "LIQUIDATE":
        liquidation_partner = find_best_liquidator(category, quantity)
        if liquidation_partner:
            liquidator_row = liquidator_df[liquidator_df["Liquidator_ID"] == liquidation_partner]
            if not liquidator_row.empty:
                target_name = liquidation_partner
                recovery_rate = liquidator_row.iloc[0]["Offer Price (% of MRP)"] / 100 # Using \'Offer Price (% of MRP)\' as recovery rate
                expected_recovery = quantity * unit_price * recovery_rate
            else:
                expected_recovery = quantity* unit_cost
    elif action == "RESELL":
        expected_recovery = quantity * unit_price 
    elif action == "CLEARANCE":
        expected_recovery = quantity * unit_price*0.7

    #Calculate tax_benefit_amount & Net loss Mitigation
    if action == "DONATE":
        tax_rate = 0.21
        tax_benefit_amount = unit_cost * tax_rate * quantity
        net_loss_mitigation = max(0, (quantity * unit_price - expected_recovery-tax_benefit_amount))
    else:
        tax_benefit_amount = 0
        net_loss_mitigation = max(0, (quantity * unit_price - expected_recovery-tax_benefit_amount))

    #Calulate gross margin percentage
    gross_margin_pct = 0 if unit_price == 0 else ((unit_price - unit_cost) / unit_price) * 100

    # Append to output records
    output_records.append({
        "return_id": return_item['return_id'],
        "store_id": store_id,
        "sku_id": return_item['sku_id'],
        "category": category,
        "return_reason": return_reason,
        "item_condition":item_condition,
        "quantity_returned": quantity,
        "days_left": days_left,
        "risk_level": risk_level,
        "recommended_action": action,
        "target_name": target_name,
        "return_date": return_item['return_date'],
        # Financial fields
        "cost_price_cp": unit_cost,
        "selling_price_sp": unit_price,
        "return_value": return_value,
        "gross_margin_pct": gross_margin_pct,
        "expected_recovery": expected_recovery,
        "tax_benefit_amount": tax_benefit_amount,
        "net_loss_mitigation": net_loss_mitigation
    })

# Create output DataFrame
output_df = pd.DataFrame(output_records)
output_df_with_issueids = assign_issue_ids(output_df)

# Save to Excel
output_filename = f"Return_Remediation_Recommendations_{timestamp}.xlsx"
output_df_with_issueids.to_excel("Output_Files/" + output_filename, index=False)

print(f"Returns processing completed. Output saved to: {output_filename}")
print(f"Total returns processed: {len(output_df)}")
print(f"Action distribution:")
print(output_df['recommended_action'].value_counts())

