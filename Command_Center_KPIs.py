import pandas as pd
from datetime import datetime
import os

def generate_shrinkage_return_kpis(shrinkage_file, return_file, output_dir="Output_Files"):
    # Load shrinkage data
    df = pd.read_excel(os.path.join(output_dir, shrinkage_file))
    
    # Remove duplicates for VERY_HIGH risk level by store_id + sku_id + cogs
    df_dedup = df.copy()
    df_dedup = df_dedup[~(
        (df_dedup["risk_level"] == "VERY_HIGH") &
        df_dedup.duplicated(subset=["store_id", "sku_id", "cogs"], keep='first')
    )]

    # Top 3 stores by shrinkage
    top3_stores = (
        df_dedup.groupby('store_id', as_index=False)
        .agg({'cogs': 'sum'})
        .sort_values('cogs', ascending=False)
        .head(3)
    )

    # Shrinkage KPIs
    filtered_df = df_dedup[df_dedup['risk_level'] != 'LOW']
    total_shrinkage = filtered_df['cogs'].sum()
    total_sales = filtered_df['original_revenue'].sum()
    shrink_perc_of_sales = ((total_sales - total_shrinkage) / total_sales) * 100 if total_sales > 0 else 0

    shrinkage_kpi = pd.DataFrame({
        "Metric": ["Total Known Shrinkage", "Total Known Sales", "Shrink % of Sales"],
        "Value": [total_shrinkage, total_sales, shrink_perc_of_sales]
    })

    # Load return data
    return_df = pd.read_excel(os.path.join(output_dir, return_file))
    return_df['sum_of_inventory'] = return_df['quantity_returned'] * return_df['cost_price_cp']

    # Top 3 root causes by return value
    top3_rootcause = (
        return_df.groupby('return_reason', as_index=False)
        .agg({'sum_of_inventory': 'sum'})
        .sort_values('sum_of_inventory', ascending=False)
        .head(3)
    )

    # Save all outputs to Excel
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"Shrinkage_and_Return_KPIs_{now}.xlsx")

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        top3_stores.to_excel(writer, index=False, sheet_name='Top3_Stores_Shrinkage')
        shrinkage_kpi.to_excel(writer, index=False, sheet_name='Shrinkage_KPIs')
        top3_rootcause.to_excel(writer, index=False, sheet_name='Top3_Return_Reasons')

    print(f"✅ KPI Report saved to: {output_path}")


generate_shrinkage_return_kpis(
    shrinkage_file="Remediation_Recommendations_20250826_154915.xlsx",
    return_file="Return_Remediation_Recommendations_20250826_144259.xlsx"
)

