import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- Load the data files ---
shrinksense_file = "Output_Files/" + "ShrinkSense_Complete_System_20250829_171131.xlsx"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Load required sheets
inventory_df = pd.read_excel(shrinksense_file, sheet_name="inventory")
stores_df = pd.read_excel(shrinksense_file, sheet_name="stores")
ngo_df = pd.read_excel(shrinksense_file, sheet_name="ngo_partners")
liquidator_df = pd.read_excel(shrinksense_file, sheet_name="liquidation_partners")
freight_cost = 0.5

def haversine_distance(lat1, lon1, lat2, lon2):
    import math
    R = 3959  # Radius of Earth in miles
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    dlon, dlat = lon2_rad - lon1_rad, lat2_rad - lat1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c



# def calculate_time_risk(days_to_expiry, total_shelf_life):
#     if total_shelf_life == 0: return 0.0
#     if days_to_expiry <= 0: return 1.0
#     return 1 - (days_to_expiry / total_shelf_life)

def calculate_time_risk(days_to_expiry, total_shelf_life, units_sold, days_active, inventory_on_hand, projected_sales_remaining):
    """
    Measures risk that stock won't clear before expiry based on velocity.
    """
    if total_shelf_life <= 0:
        return 0.0
    
    if days_to_expiry <= 0:
        return 1.0  # already expired

    # # Velocity: units sold per day
    # sell_through_per_day = units_sold / days_active if days_active > 0 else 0

    # # Projected units sold until expiry
    # projected_sales_remaining = sell_through_per_day * days_to_expiry

    # If projected sales >= current inventory, low time risk
    if projected_sales_remaining >= inventory_on_hand:
        return 0.0
    else:
        # Risk increases as gap between projected sales & inventory grows
        shortage_ratio = (inventory_on_hand - projected_sales_remaining) / inventory_on_hand
        return min(1.0, shortage_ratio)


#Change the formula
def calculate_sales_risk(units_sold, quantity_received, target_sell_through):
    if quantity_received == 0: return 0.0
    actual_sell_through = units_sold / quantity_received
    return max(0, target_sell_through - actual_sell_through) / target_sell_through if target_sell_through > 0 else 0.0

def calculate_risk_level(days_to_expiry, total_shelf_life, units_sold, quantity_received, sell_through_target,category, days_active, inventory_on_hand, projected_sales_remaining):
    time_risk = calculate_time_risk(days_to_expiry, total_shelf_life, units_sold, days_active, inventory_on_hand, projected_sales_remaining)
    sales_risk = calculate_sales_risk(units_sold, quantity_received, sell_through_target)

    # Default weighting: 70% time risk, 30% sales risk
    risk = (0.7 * time_risk) + (0.3 * sales_risk)

    if projected_sales_remaining >= inventory_on_hand:
        return "LOW"
    else:
        if category == "Fresh Produce":
            if risk > 0.9:
                return "CRITICAL"
            elif risk > 0.7:
                return "VERY_HIGH"
            elif risk >= 0.5:
                return "HIGH"
            elif risk >= 0.3:
                return "MEDIUM"
            elif risk >= 0.0:
                return "LOW"
        elif category == "Dry Goods":
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
            

def normalize(series, invert=False):
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        return pd.Series([1]*len(series))
    if invert:
        return (max_val - series) / (max_val - min_val)
    else:
        return (series - min_val) / (max_val - min_val)

def find_best_reallocation_store(store_id, sku_sell_through):
    candidate_stores = stores_df.copy()
    candidate_stores = candidate_stores[candidate_stores["Store_ID"] != store_id]
    if candidate_stores.empty:
        return None
    #Update Transportation Cost
    # Calculate dummy Euclidean distance as actual route is not definitive
    store_row = stores_df[stores_df["Store_ID"] == store_id].iloc[0]
    candidate_stores["Distance"] = candidate_stores.apply(
        lambda x: np.sqrt((x["Latitude"] - store_row["Latitude"])**2 + (x["Longitude"] - store_row["Longitude"])**2), axis=1)
    candidate_stores["Sell-through"] = sku_sell_through
    candidate_stores["Inventory"] = candidate_stores["Current_Capacity"]
    candidate_stores["DOS"] = candidate_stores["Current_Capacity"] / (sku_sell_through if sku_sell_through > 0 else 1)
    candidate_stores["Markdown %"] = 0.1  # If not available, use a constant

    weights = {"Sell-through":0.4, "Inventory":0.25, "Distance":0.2, "DOS":0.1, "Markdown %":0.05}

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
    best_store_id = best_store.iloc[0]["Store_ID"] if not best_store.empty else None
    # best_store_distance = best_store.iloc[0]["Distance_norm"] if not best_store.empty else None
    return best_store_id
    # return best_store.iloc[0]["Store_ID"] if not best_store.empty else None

#Check real data
def find_best_donation_center(category, quantity):
    eligible_ngos = ngo_df[(ngo_df["Acceptance_Criteria_Met"] == True) & (ngo_df["NGO_Type"].str.contains(category))]
    if eligible_ngos.empty:
        return None
    # Distance and past success are not available in data, so we just use capacity as proxy
    eligible_ngos = eligible_ngos.sort_values("Acceptance_Capacity_Dry_Goods", ascending=False) # Using Dry Goods as a proxy for now
    return eligible_ngos.iloc[0]["NGO_ID"]

#Check real data
def find_best_liquidator(category, quantity):
    eligible_liqs = liquidator_df[(liquidator_df["Offer Price (% of MRP)"] > 0) & (liquidator_df["Liquidator_Type"].str.contains(category))]
    if eligible_liqs.empty:
        return None
    eligible_liqs = eligible_liqs.sort_values("Offer Price (% of MRP)", ascending=False)
    return eligible_liqs.iloc[0]["Liquidator_ID"]

def get_store_sell_through_rate(store_id):
    """Get the sell through rate of a specific store"""
    store_row = stores_df[stores_df["Store_ID"] == store_id]
    if not store_row.empty:
        # Assuming there\'s a sell_through_rate column in stores_df, if not, use average from inventory
        if "Sell_Through_Rate" in stores_df.columns:
            return store_row.iloc[0]["Sell_Through_Rate"]
        else:
            # Calculate average sell through rate for items in this store
            store_items = inventory_df[inventory_df["Store_ID"] == store_id]
            if not store_items.empty:
                return store_items["Sell_Through_Rate"].mean()
    return 0.5  # Default fallback rate


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
        by=["cogs", "quantity_on_hand", "shelf_life_remaining"],
        ascending=[False, False, True],
        inplace=True
    )

    # Step 3: Assign group key
    df_filtered["group_key"] = np.where(
        df_filtered["risk_level"] == "VERY_HIGH",
        df_filtered["sku_id"].astype(str) + "_" + df_filtered["cogs"].astype(str),
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



output_records = []


for idx, item in inventory_df.iterrows():
    # Calculate risk level using the new columns
    days_to_expiry = (pd.to_datetime(item["Expiry_Date"]) - pd.to_datetime("today")).days
    total_shelf_life = item["Shelf_Life"]
    units_sold = item["Unit_Sold"]
    quantity_received = item["Actual_Quantity_Received"]
    sell_through_rate_risk = item["Sell_Through_Rate_Per_Day"]
    category = item["Category"]
    days_active = item["Days_Active"]
    inventory_on_hand = item["Inventory_On_Hand"]

    # Velocity: units sold per day
    sell_through_per_day = units_sold / days_active if days_active > 0 else 0

    # Projected units sold until expiry
    projected_sales_remaining = sell_through_per_day * days_to_expiry

    
    
    risk_level = calculate_risk_level(days_to_expiry, total_shelf_life, units_sold, quantity_received, sell_through_rate_risk,category, days_active, inventory_on_hand, projected_sales_remaining)

    stock_qty = item["Inventory_On_Hand"]
    shelf_life_remaining = item["Shelf_Life_Remaining"]
    store_id = item["Store_ID"]
    action, target_name, distance = None, None, None

    # Get markdown percentage and upliftment factor from the Excel file
    required_markdown_pct = item["Required_Markdown_Pct"] if "Required_Markdown_Pct" in item else 0.15 # Default to 15%
    required_markdown_pct = round(required_markdown_pct, 2)
    
    predicted_upliftment_factor = item["Predicted_Upliftment_Factor"] if "Predicted_Upliftment_Factor" in item else 1.15 # Default to 1.15
    predicted_upliftment_factor = round(predicted_upliftment_factor, 2)

    # Financial calculations with dynamic clearance rates
    unit_cost = item.get("Cost_Price_CP", 0)
    unit_price = item.get("Selling_Price_SP", 0)
    original_revenue = item.get("Original_Revenue(no return/remediation)", 0)
    cogs = item.get("COGS", 0)
    original_gross_margin = item.get("Original_Gross_Margin", 0)
    
    # gross_margin_pct = 0 if unit_price == 0 else ((unit_price - unit_cost) / unit_price) * 100
    # potential_gross_loss = stock_qty * (unit_price - unit_cost)  # This will be net margin not gross loss

    if shelf_life_remaining <= 2:
        risk_level = "CRITICAL"
        action = "DISPOSE"
        action_quantity = stock_qty
        
    elif risk_level == "CRITICAL":
        action = "DISPOSE"
        action_quantity = stock_qty
        
    elif risk_level == "VERY_HIGH":
        # Suggest two recommendations - Donate & Liquidation
        # Get both donation and liquidation options
        donation_center = find_best_donation_center(category, stock_qty)
        liquidation_partner = find_best_liquidator(category, stock_qty)
        # print(donation_center)
        if donation_center:
            # Create two separate recommendations
            # First recommendation: DONATE
            action_1 = "DONATE"
            target_name_1 = donation_center
            action_quantity = stock_qty
            
            # Calculate expected recovery for donation
            expected_recovery_1 = 0  # No direct revenue from donation
            if donation_center:
                ngo_row = ngo_df[ngo_df["NGO_ID"] == donation_center]
                if not ngo_row.empty:
                    # Use IRS enhanced deduction formula
                    cost_price = item.get("Cost_Price_CP", 0)
                    selling_price = item.get("Selling_Price_SP", 0)
                    action_quantity = stock_qty
                    tax_rate = 0.21  # Or your configured corporate tax rate

                    # Calculate estimated tax savings by applying tax rate
                    tax_benefit_amount_1 = tax_rate * action_quantity  #cost_price * 
                else:
                    tax_benefit_amount_1 = 0
            else:
                tax_benefit_amount_1 = 0
            
            net_loss_mitigation_1 = tax_benefit_amount_1 #max(0, original_revenue - (stock_qty * unit_price - expected_recovery_1 - tax_benefit_amount_1))
            net_loss_mitigation_1 = round(net_loss_mitigation_1, 2)
            
            # Add first recommendation (DONATE)
            output_records.append({
                "sku_id": item["SKU_ID"],
                "product_name": item["Product_Name"],
                "category": category,
                "store_id": store_id,
                "received_date": item["Received_Date"],
                "quantity_on_hand": stock_qty,
                "sell_through_rate": item["Sell_Through_Rate"],
                "Sell_Through_Rate_Per_Day": item["Sell_Through_Rate_Per_Day"],
                "shelf_life_remaining": shelf_life_remaining,
                "inventory_age_days": item["Inventory_Age_Days"],
                "shrinkage_risk": risk_level, # Using risk_level as shrinkage_risk
                "risk_level": risk_level,
                "recommended_action": action_1,
                "action_quantity": action_quantity,    
                "target_name": target_name_1,
                "recommendation_rank": 1,  # New field to indicate primary recommendation
                "unit_cost": unit_cost,
                "unit_price": unit_price,
                "original_revenue": original_revenue,
                "cogs": cogs,
                "gross_margin_pct": original_gross_margin,
                "expected_recovery": expected_recovery_1,
                "net_loss_mitigation": net_loss_mitigation_1,
                "tax_benefit_amount": tax_benefit_amount_1,
                "upliftment": predicted_upliftment_factor
            })
        if liquidation_partner:    
            # Second recommendation: LIQUIDATE
            action_2 = "LIQUIDATE"
            target_name_2 = liquidation_partner
            action_quantity = stock_qty
            
            # Calculate expected recovery for liquidation
            liquidator_row = liquidator_df[liquidator_df["Liquidator_ID"] == liquidation_partner]
            if not liquidator_row.empty:
                # breakpoint()
                recovery_rate = liquidator_row.iloc[0]["Offer Price (% of MRP)"] / 100 # Using \'Offer Price (% of MRP)\' as recovery rate
                expected_recovery_2 = stock_qty * recovery_rate  #unit_price *
            else:
                expected_recovery_2 = stock_qty * unit_cost
            
            tax_benefit_amount_2 = 0  # No tax benefit for liquidation
            net_loss_mitigation_2 = expected_recovery_2  #max(0, original_revenue - (stock_qty * unit_price - expected_recovery_2))
            net_loss_mitigation_2 = round(net_loss_mitigation_2, 2)
            
            # Add second recommendation (LIQUIDATE)
            output_records.append({
                "sku_id": item["SKU_ID"],
                "product_name": item["Product_Name"],
                "category": category,
                "store_id": store_id,
                "received_date": item["Received_Date"],
                "quantity_on_hand": stock_qty,
                "sell_through_rate": item["Sell_Through_Rate"],
                "Sell_Through_Rate_Per_Day": item["Sell_Through_Rate_Per_Day"],
                "shelf_life_remaining": shelf_life_remaining,
                "inventory_age_days": item["Inventory_Age_Days"],
                "shrinkage_risk": risk_level, # Using risk_level as shrinkage_risk
                "risk_level": risk_level,
                "recommended_action": action_2,
                "action_quantity": action_quantity,    
                "target_name": target_name_2,
                "recommendation_rank": 2,  # Second recommendation
                "unit_cost": unit_cost,
                "unit_price": unit_price,
                "original_revenue": original_revenue,
                "cogs": cogs,
                "gross_margin_pct": original_gross_margin,
                "expected_recovery": expected_recovery_2,
                "net_loss_mitigation": net_loss_mitigation_2,
                "tax_benefit_amount": tax_benefit_amount_2,
                "upliftment": predicted_upliftment_factor
            })
            
            continue

    elif risk_level == "HIGH":
        markdown_percentage = required_markdown_pct #float(action.split("_")[1].replace("%", "")) / 100
        clearance_rate = (1 - markdown_percentage) * predicted_upliftment_factor
    
        uplifted_sell_through = item["Sell_Through_Rate_Per_Day"] * (1 + predicted_upliftment_factor)
        days_left = shelf_life_remaining #item["Days_To_Expiry"]
    
        qty_clearance_source = min(stock_qty, int(uplifted_sell_through * days_left))
        qty_transfer = stock_qty - qty_clearance_source

        action = ""
        target_name = ""
        action_quantity = ""

         # If transfer needed
        if qty_transfer > 0:
            # breakpoint()
            best_store = find_best_reallocation_store(store_id, item["Sell_Through_Rate"])
            if best_store:
                action = f"Inter Store Transfer"
                target_name = best_store
                action_quantity = str(stock_qty)
    
                src_row = stores_df[stores_df["Store_ID"] == store_id].iloc[0]
                tgt_row = stores_df[stores_df["Store_ID"] == target_name].iloc[0]
                
                distance_miles = haversine_distance(
                    src_row["Latitude"], src_row["Longitude"],
                    tgt_row["Latitude"], tgt_row["Longitude"]
                )
                transport_cost = freight_cost * distance_miles
                expected_recovery = (stock_qty * unit_price) - transport_cost
            else:
                action = f"CLEARANCE_{int(markdown_percentage * 100)}%"
                target_name = f"Upliftment {(1+ predicted_upliftment_factor)}"
                expected_recovery = stock_qty * unit_price * clearance_rate
                action_quantity = str(stock_qty)
            
        else:
            action = f"CLEARANCE_{int(markdown_percentage * 100)}%"
            target_name = f"Upliftment {(1+ predicted_upliftment_factor)}"
            expected_recovery = stock_qty * unit_price * clearance_rate
            action_quantity = str(stock_qty)
            
            

    elif risk_level == "MEDIUM":
        if category == "General Merchandise":
            best_store = find_best_reallocation_store(store_id, item["Sell_Through_Rate"])
            if best_store:
                action = "Inter Store Transfer"
                target_name = best_store
                action_quantity = stock_qty
            else:
                action = f"CLEARANCE_{int(required_markdown_pct * 100)}%"
                target_name = f"Upliftment {(1+ predicted_upliftment_factor)}"

                uplifted_sell_through = item["Sell_Through_Rate_Per_Day"] * (1 + predicted_upliftment_factor)
                days_left = shelf_life_remaining
                qty_clearance_source = min(stock_qty, int(uplifted_sell_through * days_left))
                action_quantity = str(qty_clearance_source)
                
        else:
            action = f"CLEARANCE_{int(required_markdown_pct * 100)}%"
            target_name = f"Upliftment {(1+ predicted_upliftment_factor)}"

            uplifted_sell_through = item["Sell_Through_Rate_Per_Day"] * (1 + predicted_upliftment_factor)
            days_left = shelf_life_remaining
            qty_clearance_source = min(stock_qty, int(uplifted_sell_through * days_left))
            action_quantity = str(qty_clearance_source)
            
    else:
        action = "NO_ACTION"

    # Calculate expected recovery revenue with dynamic clearance rates
    expected_recovery = 0
    if action == "CLEARANCE":
        markdown_percentage = float(action.split("_")[1].replace("%", "")) / 100
        clearance_rate = (1 - markdown_percentage) * predicted_upliftment_factor
        uplifted_sell_through = item["Sell_Through_Rate_Per_Day"] * (1 + predicted_upliftment_factor)
        days_left = shelf_life_remaining #item["Days_To_Expiry"]
        qty_clearance_source = min(stock_qty, int(uplifted_sell_through * days_left))
        qty_transfer = 0
        expected_recovery_clearance = qty_clearance_source * unit_price * clearance_rate
        expected_recovery_transfer = 0
        expected_recovery = expected_recovery_clearance

        action_quantity = str(qty_clearance_source)
        
    elif action == "IST+CLEARANCE":
        markdown_percentage = float(action.split("_")[1].replace("%", "")) / 100
        clearance_rate = (1 - markdown_percentage) * predicted_upliftment_factor

        uplifted_sell_through = item["Sell_Through_Rate_Per_Day"] * (1 + predicted_upliftment_factor)
        days_left = shelf_life_remaining #item["Days_To_Expiry"]

        qty_clearance_source = min(stock_qty, int(uplifted_sell_through * days_left))
        qty_transfer = stock_qty - qty_clearance_source

        expected_recovery_clearance = qty_clearance_source * unit_price * clearance_rate

        src_row = stores_df[stores_df["Store_ID"] == store_id].iloc[0]
        tgt_row = stores_df[stores_df["Store_ID"] == target_name].iloc[0]
        distance_miles = haversine_distance(
            src_row["Latitude"], src_row["Longitude"],
            tgt_row["Latitude"], tgt_row["Longitude"]
        )
        transport_cost = freight_cost * distance_miles * qty_transfer
        expected_recovery_transfer = (qty_transfer * unit_price) - transport_cost

        expected_recovery = expected_recovery_transfer + expected_recovery_clearance
        
    elif action == "Inter Store Transfer":
        relocate_clearance = get_store_sell_through_rate(target_name)
        # Get coordinates
        src_row = stores_df[stores_df["Store_ID"] == store_id].iloc[0]
        tgt_row = stores_df[stores_df["Store_ID"] == target_name].iloc[0]
        distance_miles = haversine_distance(src_row["Latitude"], src_row["Longitude"], tgt_row["Latitude"], tgt_row["Longitude"])
        transport_cost = freight_cost * distance_miles
        expected_recovery = (stock_qty * unit_price) - transport_cost
        
    if action == "DONATE":
        expected_recovery = 0
        
    elif action == "LIQUIDATE":
        # Assuming a default recovery rate for liquidation if not specified in liquidator_df
        liquidator_row = liquidator_df[liquidator_df["Liquidator_ID"] == target_name]
        recovery_rate = liquidator_row.iloc[0]["Offer Price (% of MRP)"] / 100 if not liquidator_row.empty else 0.3
        expected_recovery = stock_qty * unit_price * recovery_rate
    elif action == "DISPOSE":
        expected_recovery = 0
    elif action == "NO_ACTION":
        expected_recovery = stock_qty * unit_price * item["Sell_Through_Rate"]  # Normal sales assumed
    else:
        expected_recovery = stock_qty * unit_price * item["Sell_Through_Rate"]

    # Calculate tax benefit amount, relevant only for donation action
    tax_benefit_amount = 0
    # Inside your donation calculation logic in final_logic.py:

    # Calculate potential net loss mitigation (positive means less loss)
    net_loss_mitigation = max(0, original_revenue - (stock_qty * unit_price - expected_recovery - tax_benefit_amount))

    # Determine action_quantity first
    try:
        action_quantity_value = action_quantity
    except NameError:
        action_quantity_value = f"issue_{stock_qty}"
    
    output_records.append({
        "sku_id": item["SKU_ID"],
        "product_name": item["Product_Name"],
        "category": category,
        "store_id": store_id,
        "received_date": item["Received_Date"],
        "quantity_on_hand": stock_qty,
        "sell_through_rate": item["Sell_Through_Rate"],
        "Sell_Through_Rate_Per_Day": item["Sell_Through_Rate_Per_Day"],
        "shelf_life_remaining": shelf_life_remaining,
        "inventory_age_days": item["Inventory_Age_Days"],
        "shrinkage_risk": risk_level, # Using risk_level as shrinkage_risk
        "risk_level": risk_level,
        "recommended_action": action,
        "target_name": target_name,
        "action_quantity": action_quantity_value, 
        # Financial fields appended
        "unit_cost": unit_cost,
        "unit_price": unit_price,
        "original_revenue": original_revenue,
        "cogs": cogs,
        "gross_margin_pct": original_gross_margin,
        "expected_recovery": expected_recovery,
        "net_loss_mitigation": net_loss_mitigation,
        "tax_benefit_amount": tax_benefit_amount,
        "upliftment": predicted_upliftment_factor
    })

output_df = pd.DataFrame(output_records)
output_df_with_issueids = assign_issue_ids(output_df)
print(output_df_with_issueids.shape)


output_filename = f"Remediation_Recommendations_{timestamp}.xlsx"
output_df_with_issueids.to_excel('Output_Files/' + output_filename, index=False)
print("Remedition Recommendation is completed successfully!!")

