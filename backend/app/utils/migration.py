"""
Enhanced migration utility for ShrinkSense
Integrates Excel data migration with the main application
"""

import pandas as pd
import sqlite3
import os
from datetime import datetime
import logging
from sqlalchemy.orm import Session
from app.database import (
    engine, ProductMaster, Store, NGOPartner, LiquidationPartner, 
    Inventory, Returns, RemediationRecommendation, ReturnRemediation
)
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class ShrinkSenseMigrator:
    def __init__(self):
        self.excel_files = {
            'main': settings.EXCEL_FILE_PATH,
            'kpi': settings.KPI_FILE_PATH,
            'remediation': settings.REMEDIATION_FILE_PATH,
            'return_remediation': settings.RETURN_REMEDIATION_FILE_PATH,
            'shrinkage_kpis': settings.SHRINKAGE_RETURN_KPIS_FILE_PATH
        }
        
    def migrate_sheet_to_sqlalchemy(self, sheet_name: str, model_class, df: pd.DataFrame):
        """Migrate DataFrame to SQLAlchemy model"""
        with Session(engine) as session:
            try:
                records = []
                
                # Get model column names (lowercase)
                model_columns = {col.name.lower(): col.name for col in model_class.__table__.columns}
                
                for _, row in df.iterrows():
                    # Convert row to dict and clean NaN values
                    row_dict = row.to_dict()
                    cleaned_dict = {}
                    
                    for k, v in row_dict.items():
                        # Normalize column name (lowercase, replace spaces/special chars)
                        normalized_key = k.lower().replace(' ', '_').replace('-', '_')
                        
                        # Map to actual model column name
                        if normalized_key in model_columns:
                            actual_key = model_columns[normalized_key]
                            cleaned_dict[actual_key] = v if pd.notna(v) else None
                    
                    # Only create record if we have the required fields
                    if cleaned_dict:
                        try:
                            record = model_class(**cleaned_dict)
                            records.append(record)
                        except TypeError as e:
                            logger.error(f"Error creating {model_class.__name__} record: {e}")
                            continue
                
                # Bulk insert with conflict handling
                if records:
                    for record in records:
                        session.merge(record)  # Use merge instead of add to handle duplicates
                    session.commit()
                    
                logger.info(f"Migrated {len(records)} records to {model_class.__tablename__}")
                return len(records)
                
            except Exception as e:
                session.rollback()
                logger.error(f"Error migrating {sheet_name}: {e}")
                return 0
    
    def migrate_excel_file(self, file_path: str):
        """Migrate single Excel file"""
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            return 0
        
        total_records = 0
        
        try:
            # Read Excel file
            excel_data = pd.read_excel(file_path, sheet_name=None)
            
            # Sheet mapping to models
            sheet_mappings = {
                'product_master': ProductMaster,
                'stores': Store,
                'ngo_partners': NGOPartner,
                'liquidation_partners': LiquidationPartner,
                'inventory': Inventory,
                'returns': Returns
            }
            
            # Migrate each sheet
            for sheet_name, df in excel_data.items():
                if sheet_name.lower() in sheet_mappings:
                    model_class = sheet_mappings[sheet_name.lower()]
                    records = self.migrate_sheet_to_sqlalchemy(sheet_name, model_class, df)
                    total_records += records
                else:
                    logger.info(f"Skipping unmapped sheet: {sheet_name}")
            
            return total_records
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return 0
    
    def migrate_remediation_data(self, file_path: str):
        """Migrate remediation recommendations"""
        if not os.path.exists(file_path):
            return 0
        
        try:
            df = pd.read_excel(file_path)
            return self.migrate_sheet_to_sqlalchemy('remediation', RemediationRecommendation, df)
        except Exception as e:
            logger.error(f"Error migrating remediation data: {e}")
            return 0
    
    def migrate_return_remediation_data(self, file_path: str):
        """Migrate return remediation data"""
        if not os.path.exists(file_path):
            return 0
        
        try:
            df = pd.read_excel(file_path)
            return self.migrate_sheet_to_sqlalchemy('return_remediation', ReturnRemediation, df)
        except Exception as e:
            logger.error(f"Error migrating return remediation data: {e}")
            return 0
    
    def run_full_migration(self):
        """Run complete migration process"""
        logger.info("Starting data migration...")
        total_records = 0
        
        # Migrate main Excel file
        if self.excel_files['main']:
            records = self.migrate_excel_file(self.excel_files['main'])
            total_records += records
            logger.info(f"Main file migrated: {records} records")
        
        # Migrate remediation files
        if self.excel_files['remediation']:
            records = self.migrate_remediation_data(self.excel_files['remediation'])
            total_records += records
            logger.info(f"Remediation data migrated: {records} records")
        
        if self.excel_files['return_remediation']:
            records = self.migrate_return_remediation_data(self.excel_files['return_remediation'])
            total_records += records
            logger.info(f"Return remediation data migrated: {records} records")
        
        logger.info(f"Migration completed. Total records: {total_records}")
        return total_records

def run_migration():
    """Run the migration process"""
    migrator = ShrinkSenseMigrator()
    return migrator.run_full_migration()