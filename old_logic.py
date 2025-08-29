#import libraries
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

shrinksense_file = "Output_Files/" + "ShrinkSense_Complete_System_20250812_122053.xlsx"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

#Reading data
df = pd.read_excel(shrinksense_file ,sheet_name=None)

df_inve = df["inventory"]
df_returns = df["returns"]
df_stores = df["stores"]
df_ngo = df["ngo_partners"]
df_liquidators = df["liquidation_partners"]

#Inventory Accuracy
def inventory_accuracy(data, category):
    filtered = data[data["Category"] == category].copy()
    actual_qty = filtered["Actual_Quantity_Received"].sum()
    system_qty = filtered["System_Quantity_Received"].sum()

    if system_qty == 0:
        Inv_accuracy_pct = 0  # Avoid division by zero
    else:
        Inv_accuracy_pct = (actual_qty / system_qty) * 100
        
    return Inv_accuracy_pct

#damaged_percentage
def damaged_percentage(data, category):
    filtered = data[data["Category"] == category].copy()
    actual_qty = filtered["Actual_Quantity_Received"].sum()
    damaged_qty = filtered["Number_Damaged_Units"].sum()

    if damaged_qty == 0:
        damaged_percentage = 0
    else:
        damaged_percentage = (damaged_qty/actual_qty)*100
    
    return damaged_percentage 

#dump_percentage
def dump_percentage(data, category):
    filtered = data[data["Category"] == category].copy()
    actual_qty = filtered["Actual_Quantity_Received"].sum()
    dumped_qty = filtered["Number_Dump_Units"].sum()

    if dumped_qty == 0:
        dump_percentage = 0
    else:
        dump_percentage = (dumped_qty/actual_qty)*100

    return dump_percentage

#expired_pct
def expired_percentage(data, category):
    filtered = data[data["Category"] == category].copy()
    actual_qty = filtered["Actual_Quantity_Received"].sum()
    exp_qty = filtered["Number_Expired_Units"].sum()

    if exp_qty == 0:
        expired_pct = 0
    else:
        expired_pct = (exp_qty/actual_qty)*100
    
    return expired_pct

#aged_pct_by_category
def aged_percentage(data, category):
    aged_statuses = ["Expiry Approaching", "Critical - Expiring Soon"]
    
    filtered = data[(data["Category"] == category) &
    (data["Inventory_Status"].isin(aged_statuses)) ].copy()
    
    aged_actual_qty = filtered["Actual_Quantity_Received"].sum()
    actual_qty_qty = data["Actual_Quantity_Received"].sum()

    if actual_qty_qty == 0:
        aged_pct = 0
    else:
        aged_pct = (aged_actual_qty/actual_qty_qty)*100
    
    return aged_pct

#Shrinkage %
def shrinkage_percentage(data, category):
    filtered = data[data["Category"] == category].copy()
    actual_qty = filtered["Actual_Quantity_Received"].sum()
    
    dump_units = filtered['Number_Dump_Units'].sum()
    damaged_units = filtered["Number_Damaged_Units"].sum()
    expired_units = filtered["Number_Expired_Units"].sum()

    total_shrinkage_units = dump_units + damaged_units + expired_units

    if total_shrinkage_units == 0:
        shrinkage_pct = 0
    else:
        shrinkage_pct = (total_shrinkage_units/actual_qty)*100
    
    return shrinkage_pct

    
#Return %
def return_percentage(data1, data2, category):
    filtered_inv = data1[data1["Category"] == category].copy()
    filtered_return = data2[data2["category"] == category]
    actual_units_sold = filtered_inv["Unit_Sold"].sum()
    returned_qty = filtered_return["quantity_returned"].sum()

    if returned_qty == 0:
        return_pct = 0
    else:
        return_pct = (returned_qty/actual_units_sold)*100
    return return_pct

#Waste % of Net Sales
def waste_pct_of_net_sales(data, category):
    filtered = data[data["Category"] == category].copy()
    Total_waste_value = ((filtered["Number_Dump_Units"]+filtered["Number_Damaged_Units"]+filtered["Number_Expired_Units"])*(filtered["Selling_Price(SP)"])).sum()
    Net_sales = (filtered['Actual_Quantity_Received']*filtered["Selling_Price(SP)"]).sum()
    if Total_waste_value == 0:
        waste_pct_net_sales = 0
    else:
        waste_pct_net_sales = Total_waste_value/Net_sales

    return waste_pct_net_sales



    
    
#Non-Sellable Inventory Overview
def non_sellable_inv(data, category):
    filtered = data[data["Category"] == category].copy()
    dump_units = filtered['Number_Dump_Units'].sum()
    damaged_units = filtered["Number_Damaged_Units"].sum()
    expired_units = filtered["Number_Expired_Units"].sum()

    Total_non_sellable_units = dump_units + damaged_units + expired_units
    dump_pct = (dump_units/Total_non_sellable_units)*100
    damage_pct = (damaged_units/Total_non_sellable_units)*100
    expired_pct = (expired_units/Total_non_sellable_units) *100
    return Total_non_sellable_units

#SKU’s with Highest Shrinkage by sales
def sku_highest_shrinkage(data, category):
    filtered = data[data["Category"] == category].copy()
    filtered['shrink_value'] = (filtered["Number_Damaged_Units"] + filtered["Number_Dump_Units"] + filtered["Number_Expired_Units"])*filtered["Selling_Price(SP)"]
    filtered["Total_Inv_value"] = filtered["Actual_Quantity_Received"]*filtered["Selling_Price(SP)"]

    shrink_pct = (filtered.groupby("SKU_ID")["shrink_value"].sum()/filtered.groupby("SKU_ID")["Total_Inv_value"].sum())*100

    Top_10_SKU_with_highest_shrinkage = shrink_pct.reset_index(name="Shrinkage").sort_values(by = 'Shrinkage', ascending=False).head(10)
    
    return Top_10_SKU_with_highest_shrinkage 

#Suppliers with Highest Shrinkage % by sales
def suppliers_highest_shrinkage(data, category):
    filtered = data[data["Category"] == category].copy()
    filtered['shrink_value'] = (filtered["Number_Damaged_Units"] + filtered["Number_Dump_Units"] + filtered["Number_Expired_Units"])*filtered["Selling_Price(SP)"]
    filtered["Total_Inv_value"] = filtered["Actual_Quantity_Received"]*filtered["Selling_Price(SP)"]

    shrink_pct = (filtered.groupby("Supplier_Name")["shrink_value"].sum()/filtered.groupby("Supplier_Name")["Total_Inv_value"].sum())*100

    Top_10_suppliers_with_highest_shrinkage = shrink_pct.reset_index(name="Shrinkage_pct").sort_values(by = 'Shrinkage_pct', ascending=False).head(10)
    
    return Top_10_suppliers_with_highest_shrinkage

#shrinkage % to Inventory (SKU) % Ratio
def shrink_inv_ratio(data, category):
    filtered = data[data["Category"] == category].copy()
    shrink_val_cat = (filtered["Number_Damaged_Units"] + filtered["Number_Dump_Units"] + filtered["Number_Expired_Units"]).sum()
    total_shrink_val = (data["Number_Damaged_Units"] + data["Number_Dump_Units"] + data["Number_Expired_Units"]).sum()
    cat_units = filtered["Actual_Quantity_Received"].sum()
    total_inv = data["Actual_Quantity_Received"].sum()

    shrinkage_value_pct = (shrink_val_cat/total_shrink_val)*100
    inv_pct = (cat_units/total_inv)*100
    shrink_inv_ratio = shrinkage_value_pct/inv_pct

    return shrink_inv_ratio

#Waste by Merch-Category
def wastage_by_march_cat(data, category):
    filtered = data[data["Category"] == category].copy()
    filtered["Received_Date"] = pd.to_datetime(filtered["Received_Date"])
    filtered["Month"] = filtered["Received_Date"].dt.to_period("M").astype(str)
    filtered["Total_Waste_Units"] = (
    filtered["Number_Dump_Units"] +
    filtered["Number_Damaged_Units"] +
    filtered["Number_Expired_Units"]
)
    filtered["Waste_Cost"] = filtered["Total_Waste_Units"] * filtered["Selling_Price(SP)"]
    filtered["Waste_Cost"] = filtered["Total_Waste_Units"] * filtered["Selling_Price(SP)"]

    monthly_waste_cost = filtered.groupby("Month")["Waste_Cost"].sum().reset_index()
    monthly_waste_cost.columns = ["Month", "Total_Waste_Cost"]

    return monthly_waste_cost

#Sales vs Shrinkage % vs Salvage %


categories = ["Fresh Produce","General Merchandise","Dry Goods"]
#Calling functions
kpi_summary = []

for category in categories:
    inventory_acc = inventory_accuracy(df_inve, category)
    damage_pct = damaged_percentage(df_inve, category)
    dump_pct = dump_percentage(df_inve, category)
    expir_pct = expired_percentage(df_inve, category)
    aged_pct = aged_percentage(df_inve, category)
    shrink_pct = shrinkage_percentage(df_inve, category)
    return_pct = return_percentage(df_inve, df_returns, category)
    
    waste_pct_of_net_sales = waste_pct_of_net_sales(df_inve, category)
    nse = non_sellable_inv(df_inve, category)
    si_ratio = shrink_inv_ratio(df_inve, category)
    #monthly_wastage = wastage_by_march_cat(df_inve, category)

    # Convert DataFrames to dictionaries
    swhs = sku_highest_shrinkage(df_inve, category).to_dict(orient='records')
    su_hs = suppliers_highest_shrinkage(df_inve, category).to_dict(orient='records')
    monthly_wastage = wastage_by_march_cat(df_inve, category).to_dict(orient='records')

    row = {
        "Category": category,
        "Inventory_Accuracy": inventory_Acc,
        "Damage_%": damage_pct,
        "Dump_%": dump_pct,
        "Expired_%": expir_pct,
        "Aged_%": aged_pct,
        "Return_%": return_pct,
        "Shrinkage_%": shrink_pct
    }

    # print(row)
    kpi_summary.append(row)
kpi_df = pd.DataFrame(kpi_summary)
print(kpi_df)

# Save to Excel
output_filename = "Output_Files/" + "Retail_Leader_Board_KPIs.xlsx"
kpi_df.to_excel(output_filename, index=False)
