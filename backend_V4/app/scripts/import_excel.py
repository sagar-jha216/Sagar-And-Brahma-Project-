#     run()
import pandas as pd
import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('shrink_sense.db')
cursor = conn.cursor()

# Define Excel files and sheet-to-table mappings
excel_files = {
    "ShrinkSense_Complete_System_20250807_173012.xlsx": {
        "inventory": "inventory",
        "stores": "stores",
        "ngo_partners": "ngo_partners",
        "liquidation_partners": "liquidation_partners",
        "returns": "returns"
    },
    "return_remediation.xlsx": {
        "Sheet1": "return_remediation"
    },
    "remediation_recommendations.xlsx": {
        "Sheet1": "remediation_recommendations"
    },
    "Retail_Leader_Board_KPIs.xlsx": {
        "Sheet1": "retail_kpi" 
    }
}


# Function to clean column names
def clean_columns(df):
    df.columns = (
        df.columns.str.strip()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
    )
    return df

# Function to fix datetime objects (convert to string)
def convert_types(df):
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].astype(str) # Convert datetime to string
    return df

# Loop through each file and sheet
for file_name, sheets in excel_files.items():
    for sheet_name, table_name in sheets.items():
        print(f"📥 Importing {sheet_name} from {file_name} into {table_name}...")

        # Read Excel sheet
        df = pd.read_excel(file_name, sheet_name=sheet_name, engine="openpyxl")

        # Clean and convert data
        df = clean_columns(df)
        df = convert_types(df)

        # Build SQL insert query (with INSERT OR IGNORE)
        cols = ",".join(df.columns)
        placeholders = ",".join("?" * len(df.columns))
        query = f"INSERT OR IGNORE INTO {table_name} ({cols}) VALUES ({placeholders})"

        # Insert data
        cursor.executemany(query, df.values.tolist())
        conn.commit()

print("✅ Import completed successfully (duplicates skipped).")