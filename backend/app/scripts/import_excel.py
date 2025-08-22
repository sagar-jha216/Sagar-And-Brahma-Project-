import pandas as pd
import sys
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal  # works with sys.path fix
from app.models.inventory import Inventory  
from app.models.stores import Store
from app.models.ngo_partners import NGOPartner
from app.models.liquidation_partners import LiquidationPartner
from app.models.returns import Return
from app.models.return_remediation import ReturnRemediation
from app.models.remediation_recommendations import RemediationRecommendation

# Load Excel file
file_path_1 = "ShrinkSense_Complete_System_20250807_173012.xlsx"
file_path_2 = "Return_Remediation_Recommendations_20250807_173301.xlsx"
file_path_3 = "Remediation_Recommendations_20250807_173351.xlsx"

# Load sheets
inventory_df = pd.read_excel(file_path_1, sheet_name="inventory")
stores_df = pd.read_excel(file_path_1, sheet_name="stores")
ngo_df = pd.read_excel(file_path_1, sheet_name="ngo_partners")
liquidation_df = pd.read_excel(file_path_1, sheet_name="liquidation_partners")
returns_df = pd.read_excel(file_path_1, sheet_name="returns")

return_remediation_df = pd.read_excel(file_path_2)
recommendation_df = pd.read_excel(file_path_3)

# Convert dates and booleans
date_columns = ["Received_Date", "Expiry_Date", "return_date", "original_purchase_date", "created_at", "updated_at"]
for col in date_columns:
    for df in [inventory_df, returns_df, recommendation_df, return_remediation_df]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

bool_columns = ["Is_Returnable", "Is_Perishable", "Acceptance_Criteria_Met"]
for col in bool_columns:
    for df in [inventory_df, ngo_df]:
        if col in df.columns:
            df[col] = df[col].astype(bool)

# Start DB session
session: Session = SessionLocal()

# Insert inventory data
for _, row in inventory_df.iterrows():
    item = Inventory(**row.to_dict())
    session.add(item)

# Insert stores
for _, row in stores_df.iterrows():
    store = Store(**row.to_dict())
    session.add(store)

# Insert NGO partners
for _, row in ngo_df.iterrows():
    ngo = NGOPartner(**row.to_dict())
    session.add(ngo)

# Insert liquidation partners
for _, row in liquidation_df.iterrows():
    liquidation_partners = LiquidationPartner(**row.to_dict())
    session.add(liquidation_partners)

# Insert returns
for _, row in returns_df.iterrows():
    ret = Return(**row.to_dict())
    session.add(ret)

# Insert return remediations
for _, row in return_remediation_df.iterrows():
    remediation = ReturnRemediation(**row.to_dict())
    session.add(remediation)

# Insert recommendations
for _, row in recommendation_df.iterrows():
    rec = RemediationRecommendation(**row.to_dict())
    session.add(rec)

# Commit all
session.commit()
session.close()


