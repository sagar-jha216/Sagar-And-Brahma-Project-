#import libraries
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# shrinksense_file = "Output_Files/OLD/" + "ShrinkSense_Complete_System_20250812_122053.xlsx"
shrinksense_file = "Output_Files/" + "ShrinkSense_Complete_System_20250826_140558.xlsx"
remediation_file = "Output_Files/" + "Remediation_Recommendations_20250826_154915.xlsx"

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

#Reading data
df = pd.read_excel(shrinksense_file ,sheet_name=None)

rem_df = pd.read_excel(remediation_file ,sheet_name="Sheet1")
rem_df = rem_df[rem_df['recommendation_rank']!=1]
rem_df = rem_df[['sku_id', 'store_id', 'category', 'received_date', 'quantity_on_hand', 'recommended_action', 'net_loss_mitigation']]
                 

df_inve = df["inventory"]
df_returns = df["returns"]
df_stores = df["stores"]
df_ngo = df["ngo_partners"]
df_liquidators = df["liquidation_partners"]

df_inv_remed = pd.merge(df_inve, rem_df, left_on=['SKU_ID', 'Store_ID', 'Category', 'Received_Date', 'Inventory_On_Hand'], right_on=['sku_id', 'store_id', 'category', 'received_date', 'quantity_on_hand'], how = 'inner', indicator=True)

# df2.to_excel("Join_Test.xlsx", index=False)

#Inventory Accuracy
def inventory_accuracy(data, category):
    filtered = data[data["Category"] == category].copy()
    actual_qty = filtered["Actual_Quantity_Received"].sum()
    system_qty = filtered["System_Quantity_Received"].sum()

    if system_qty == 0:
        inv_accuracy_pct = 0  # Avoid division by zero
    else:
        inv_accuracy_pct = (actual_qty / system_qty) * 100
        
    return inv_accuracy_pct
    

#damaged_percentage
def damaged_percentage(data, category):
    filtered = data[data["Category"] == category].copy()
    actual_qty = filtered["Actual_Quantity_Received"].sum()
    damaged_qty = filtered["Number_Damaged_Units"].sum()

    if damaged_qty == 0:
        damaged_percentage = 0
    else:
        damaged_percentage = (damaged_qty/actual_qty)*100

    print("Damaged Percentage", round(damaged_percentage, 2))
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

    print("Dump Percentage", round(dump_percentage, 2))
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

    print("Expired Percentage", round(expired_pct, 2))
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
    total_shrinkage_units = filtered["Difference_(System - Actual)"].sum()

    if total_shrinkage_units == 0:
        shrinkage_pct = 0
    else:
        shrinkage_pct = (total_shrinkage_units/actual_qty)*100
    
    return shrinkage_pct


#Waste %
def waste_percentage(data, category):
    filtered = data[data["Category"] == category].copy()
    actual_qty = filtered["Actual_Quantity_Received"].sum()
    
    dump_units = filtered['Number_Dump_Units'].sum()
    damaged_units = filtered["Number_Damaged_Units"].sum()
    expired_units = filtered["Number_Expired_Units"].sum()

    total_waste_units = dump_units + damaged_units + expired_units

    if total_waste_units == 0:
        wastage_pct = 0
    else:
        wastage_pct = (total_waste_units/actual_qty)*100
    
    return wastage_pct

    
#Return %
def return_percentage(data1, data2, category):
    filtered_inv = data1[data1["Category"] == category].copy()
    filtered_return = data2[data2["category"] == category]
    actual_units_sold = filtered_inv["Unit_Sold"].sum()
    returned_qty = filtered_return["quantity_returned"].sum()

    if returned_qty == 0:
        return_pct = 0
    else:
        try:
            return_pct = (returned_qty/actual_units_sold)*100
        except:
            return_pct = 0
    return return_pct


#Waste % of COGS
def waste_pct_of_cogs(data, category):
    filtered = data[data["Category"] == category].copy()
    
    total_waste_value = ((filtered["Number_Dump_Units"]+filtered["Number_Damaged_Units"]+filtered["Number_Expired_Units"])*(filtered["Cost_Price_CP"])).sum()
    
    cogs = (filtered['Actual_Quantity_Received']*filtered["Cost_Price_CP"]).sum()
    
    if total_waste_value == 0:
        waste_perct_cogs = 0
    else:
        waste_perct_cogs = (total_waste_value/cogs)*100

    return waste_perct_cogs


#Non-Sellable Inventory Overview
def non_sellable_inv(data, category):
    filtered = data[data["Category"] == category].copy()
    dump_units = filtered['Number_Dump_Units'].sum()
    damaged_units = filtered["Number_Damaged_Units"].sum()
    expired_units = filtered["Number_Expired_Units"].sum()

    total_non_sellable_units = dump_units + damaged_units + expired_units
    dump_pct = (dump_units/total_non_sellable_units)*100
    damage_pct = (damaged_units/total_non_sellable_units)*100
    expired_pct = (expired_units/total_non_sellable_units) *100

    return damage_pct, dump_pct, expired_pct
    


#SKU’s with Highest Shrinkage by sales
def sku_highest_shrinkage(data, category):
    filtered = data[data["Category"] == category].copy()
    
    filtered['shrink_value'] = filtered["Difference_(System - Actual)"]*filtered["Selling_Price_SP"]
    filtered["total_inv_value"] = filtered["Unit_Sold"]*filtered["Selling_Price_SP"]

    shrink_pct = (filtered.groupby("SKU_ID")["shrink_value"].sum()/filtered.groupby("SKU_ID")["total_inv_value"].sum())*100

    top_10_SKU_with_highest_shrinkage = shrink_pct.reset_index(name="Shrinkage").sort_values(by = 'Shrinkage', ascending=False).head(10)

    return top_10_SKU_with_highest_shrinkage 


#Suppliers with Highest Shrinkage % by sales
def suppliers_highest_shrinkage(data, category):
    filtered = data[data["Category"] == category].copy()
    
    filtered['shrink_value'] = filtered["Difference_(System - Actual)"]*filtered["Selling_Price_SP"]
    filtered["total_inv_value"] = filtered["Unit_Sold"]*filtered["Selling_Price_SP"]

    shrink_pct = (filtered.groupby("Supplier_Name")["shrink_value"].sum()/filtered.groupby("Supplier_Name")["total_inv_value"].sum())*100

    top_10_suppliers_with_highest_shrinkage = shrink_pct.reset_index(name="Shrinkage_pct").sort_values(by = 'Shrinkage_pct', ascending=False).head(10)

    return top_10_suppliers_with_highest_shrinkage



#Waste by Merch-Category
def sales_vs_shrink_vs_waste_vs_salv(data, category):
    filtered = data[data["Category"] == category].copy()
    
    filtered["Received_Date"] = pd.to_datetime(filtered["Received_Date"])
    filtered["Month"] = filtered["Received_Date"].dt.to_period("M").astype(str)
    
    filtered["Total_Waste_Units"] = (
    filtered["Number_Dump_Units"] +
    filtered["Number_Damaged_Units"] +
    filtered["Number_Expired_Units"]
)

    filtered["Waste"] = filtered["Total_Waste_Units"] * filtered["Selling_Price_SP"]
    filtered['Sales'] = filtered["Unit_Sold"] * filtered["Selling_Price_SP"]
    filtered["Shrinkage"] = filtered["Difference_(System - Actual)"]*filtered["Selling_Price_SP"]
    filtered["Salvage"] = filtered[filtered["recommended_action"] == 'LIQUIDATE']['net_loss_mitigation']

    monthly_wastage_by_march_cat = filtered.groupby("Month", as_index=False).agg({"Sales":'sum', 'Shrinkage':'sum', "Waste":'sum', 'Salvage':'sum'}).reset_index(drop=True)
    
    monthly_wastage_by_march_cat.columns = ["Month", "Sales", "Shrinkage", "Wastege", "Salvage"]

    return monthly_wastage_by_march_cat



#Sales vs Shrinkage % vs Salvage %
def sales_vs_shrink_vs_salv(data, category):
    filtered = data[data["Category"] == category].copy()
    # filtered = filtered[filtered["recommended_action"] == 'LIQUIDATE'].copy()
    
    filtered["Received_Date"] = pd.to_datetime(filtered["Received_Date"])
    filtered["Month"] = filtered["Received_Date"].dt.to_period("M").astype(str)

    filtered['Sales'] = filtered["Unit_Sold"] * filtered["Selling_Price_SP"]
    filtered["Shrinkage"] = filtered["Difference_(System - Actual)"]*filtered["Selling_Price_SP"]
    filtered["Salvage"] = filtered[filtered["recommended_action"] == 'LIQUIDATE']['net_loss_mitigation']

    monthly_sales_vs_shrink_vs_salv = filtered.groupby("Month", as_index=False).agg({"Sales":'sum', 'Shrinkage':'sum', 'Salvage':'sum'}).reset_index(drop=True)
    monthly_sales_vs_shrink_vs_salv.columns = ["Month", "Sales", "Shrinkage", "Salvage"]

    return monthly_sales_vs_shrink_vs_salv



def shrinkage_to_sku_ratio(data, category, sku_col="SKU_ID", shrink_col="Difference_(System - Actual)", target_pct=80):
    df = data[data["Category"] == category].copy()
    
    # Aggregate shrinkage per SKU
    shrink_by_sku = df.groupby(sku_col)[shrink_col].sum().reset_index()
    
    # Sort by shrinkage descending
    shrink_by_sku = shrink_by_sku.sort_values(shrink_col, ascending=False)
    
    # Cumulative shrinkage %
    shrink_by_sku["CUM_SHRINK_PCT"] = (
        shrink_by_sku[shrink_col].cumsum() / shrink_by_sku[shrink_col].sum() * 100
    )
    
    # Find SKU count needed to reach target shrinkage %
    sku_count = (shrink_by_sku["CUM_SHRINK_PCT"] <= target_pct).sum()
    
    # SKU %
    total_skus = shrink_by_sku[sku_col].nunique()
    sku_pct = sku_count / total_skus * 100
    
    return sku_count
    # return {
    #     "target_shrinkage_pct": target_pct,
    #     "sku_count": sku_count,
    #     "sku_pct": sku_pct,
    #     "total_skus": total_skus
    # }



    
categories = ["Fresh Produce","General Merchandise","Dry Goods"]
#Calling functions
kpi_summary = []

for category in categories:

    ## Calling Top Row KPIs
    inventory_acc = inventory_accuracy(df_inve, category)
    damage_pct = damaged_percentage(df_inve, category)
    dump_pct = dump_percentage(df_inve, category)
    expir_pct = expired_percentage(df_inve, category)
    aged_pct = aged_percentage(df_inve, category)
    shrink_pct = shrinkage_percentage(df_inve, category)
    waste_pct = waste_percentage(df_inve, category)
    return_pct = return_percentage(df_inve, df_returns, category)
    shrinkage_sku_ratio = shrinkage_to_sku_ratio(df_inve, category)
    
    # Pie Digram
    cogs_waste_pct = waste_pct_of_cogs(df_inve, category)
    damage_perct, dump_perct, expired_perct = non_sellable_inv(df_inve, category)


    # Convert DataFrames to dictionaries
    high_shrinkage_skus = sku_highest_shrinkage(df_inve, category).to_dict(orient='records')
    high_shrinkage_suppl = suppliers_highest_shrinkage(df_inve, category).to_dict(orient='records')
    sale_shrink_waste_salv = sales_vs_shrink_vs_waste_vs_salv(df_inv_remed, category).to_dict(orient='records')
    sale_shrink_salv = sales_vs_shrink_vs_salv(df_inv_remed, category).to_dict(orient='records')
    print("\n")
    
    row = {
        "Category": category,
        "Inventory_Accuracy": inventory_acc,
        "damage_percent": damage_pct,
        "dump_percent": dump_pct,
        "expired_percent": expir_pct,
        "aged_percent": aged_pct,
        "return_percent": return_pct,
        "shrinkage_percent": shrink_pct,
        "waste_percent": waste_pct
    }

    kpi_summary.append(row)
kpi_df = pd.DataFrame(kpi_summary)


# Save to Excel
output_filename = "Output_Files/" + "Retail_Leader_Board_KPIs.xlsx"
# kpi_df.to_excel(output_filename, index=False)


