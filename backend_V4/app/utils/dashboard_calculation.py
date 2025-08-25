import pandas as pd
import numpy as np

def convert_numpy_types(data):
    """Convert numpy types to native Python types for JSON serialization"""
    if isinstance(data, dict):
        return {k: convert_numpy_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_numpy_types(item) for item in data]
    elif isinstance(data, np.integer):
        return int(data)
    elif isinstance(data, np.floating):
        return float(data)
    elif isinstance(data, np.ndarray):
        return data.tolist()
    else:
        return data

def wastage_by_merch_cat(df, category=None):
    """Calculate wastage by merchandise category"""
    filtered_df = df.copy()
    if category:
        filtered_df = filtered_df[filtered_df["Category"] == category]
    
    wastage_data = filtered_df.groupby("Category").agg({
        "Number_Dump_Units": "sum",
        "Number_Damaged_Units": "sum", 
        "Number_Expired_Units": "sum",
        "Actual_Quantity_Received": "sum"
    }).reset_index()
    
    wastage_data["Total_Wastage"] = (
        wastage_data["Number_Dump_Units"] + 
        wastage_data["Number_Damaged_Units"] + 
        wastage_data["Number_Expired_Units"]
    )
    wastage_data["Wastage_Percentage"] = (
        wastage_data["Total_Wastage"] / wastage_data["Actual_Quantity_Received"] * 100
    ).astype(float)
    
    return convert_numpy_types(wastage_data.to_dict('records'))

def waste_pct_of_cogs(df, category=None):
    """Calculate waste percentage of COGS"""
    filtered_df = df.copy()
    if category:
        filtered_df = filtered_df[filtered_df["Category"] == category]
    
    total_waste_units = (
        filtered_df["Number_Dump_Units"] + 
        filtered_df["Number_Damaged_Units"] + 
        filtered_df["Number_Expired_Units"]
    ).sum()
    
    total_waste_value = (total_waste_units * filtered_df["Cost_Price_CP"]).sum()
    total_cogs = (filtered_df["Actual_Quantity_Received"] * filtered_df["Cost_Price_CP"]).sum()
    
    waste_percentage = (total_waste_value / total_cogs * 100) if total_cogs else 0
    
    return convert_numpy_types({
        "waste_value": total_waste_value,
        "total_cogs": total_cogs,
        "waste_percentage": waste_percentage
    })

def suppliers_highest_shrinkage(df, category=None):
    """Find suppliers with highest shrinkage"""
    filtered_df = df.copy()
    if category:
        filtered_df = filtered_df[filtered_df["Category"] == category]
    
    supplier_data = filtered_df.groupby("Supplier_Name").agg({
        "Number_Dump_Units": "sum",
        "Number_Damaged_Units": "sum",
        "Number_Expired_Units": "sum",
        "Actual_Quantity_Received": "sum"
    }).reset_index()
    
    supplier_data["Total_Shrinkage"] = (
        supplier_data["Number_Dump_Units"] + 
        supplier_data["Number_Damaged_Units"] + 
        supplier_data["Number_Expired_Units"]
    )
    supplier_data["Shrinkage_Percentage"] = (
        supplier_data["Total_Shrinkage"] / supplier_data["Actual_Quantity_Received"] * 100
    ).astype(float)
    
    return convert_numpy_types(supplier_data.nlargest(10, "Shrinkage_Percentage").to_dict('records'))

def non_sellable_inventory(df, category=None):
    """Calculate non-sellable inventory units"""
    filtered_df = df.copy()
    if category:
        filtered_df = filtered_df[filtered_df["Category"] == category]
    
    dump_units = filtered_df["Number_Dump_Units"].sum()
    damaged_units = filtered_df["Number_Damaged_Units"].sum()
    expired_units = filtered_df["Number_Expired_Units"].sum()
    
    return convert_numpy_types({
        "dump_units": dump_units,
        "damaged_units": damaged_units,
        "expired_units": expired_units,
        "total_non_sellable": dump_units + damaged_units + expired_units
    })

def shrink_inv_ratio(df, category=None):
    """Calculate sales vs shrinkage vs salvage ratio"""
    filtered_df = df.copy()
    if category:
        filtered_df = filtered_df[filtered_df["Category"] == category]
    
    total_received = filtered_df["Actual_Quantity_Received"].sum()
    units_sold = filtered_df["Unit_Sold"].sum()
    
    shrinkage_units = (
        filtered_df["Number_Dump_Units"] + 
        filtered_df["Number_Damaged_Units"] + 
        filtered_df["Number_Expired_Units"]
    ).sum()
    
    # Since there's no salvage column in the schema, set salvage_units to 0
    salvage_units = 0
    
    return convert_numpy_types({
        "sales_percentage": (units_sold / total_received * 100) if total_received else 0,
        "shrinkage_percentage": (shrinkage_units / total_received * 100) if total_received else 0,
        "salvage_percentage": (salvage_units / total_received * 100) if total_received else 0,
        "units_sold": units_sold,
        "shrinkage_units": shrinkage_units,
        "salvage_units": salvage_units
    })

def sku_highest_shrinkage(df, category=None):
    """Find top 10 SKUs with highest shrinkage"""
    filtered_df = df.copy()
    if category:
        filtered_df = filtered_df[filtered_df["Category"] == category]
    
    sku_data = filtered_df.groupby(["SKU_ID", "Product_Name"]).agg({
        "Number_Dump_Units": "sum",
        "Number_Damaged_Units": "sum",
        "Number_Expired_Units": "sum",
        "Actual_Quantity_Received": "sum"
    }).reset_index()
    
    sku_data["Total_Shrinkage"] = (
        sku_data["Number_Dump_Units"] + 
        sku_data["Number_Damaged_Units"] + 
        sku_data["Number_Expired_Units"]
    )
    sku_data["Shrinkage_Percentage"] = (
        sku_data["Total_Shrinkage"] / sku_data["Actual_Quantity_Received"] * 100
    ).astype(float)
    
    return convert_numpy_types(sku_data.nlargest(10, "Shrinkage_Percentage").to_dict('records'))