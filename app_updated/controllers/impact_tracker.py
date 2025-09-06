from sqlalchemy.orm import Session
from sqlalchemy import func, case, desc, and_, or_
from app.models.inventory import Inventory
from app.models.returns import Return
from app.models.stores import Store
from typing import Optional, Dict, List
from datetime import date, datetime, timedelta
import pandas as pd
from app.schemas.impact_tracker import (
    ImpactTrackerFilterParams, 
    ImpactTrackerResponse,
    SummaryData,
    SummaryComparison,
    ChartDataPoint,
    ShrinkReportRow
)

def get_impact_tracker_data(filters: ImpactTrackerFilterParams, db: Session) -> Dict:
    """
    Get impact tracker data based on filters
    """
    
    # Base query for inventory data
    inventory_query = db.query(Inventory)
    
    # Apply filters
    if filters.region:
        inventory_query = inventory_query.filter(Inventory.Region_Historical == filters.region)
    
    if filters.store_ids:
        inventory_query = inventory_query.filter(Inventory.Store_ID.in_(filters.store_ids))
    
    if filters.channels:
        inventory_query = inventory_query.filter(Inventory.Store_Channel.in_(filters.channels))
    
    if filters.selected_date:
        inventory_query = inventory_query.filter(
            func.date(Inventory.Received_Date) == filters.selected_date
        )
    
    # Get filtered data
    inventory_records = inventory_query.all()
    
    # Convert to DataFrame for easier processing
    df_inventory = pd.DataFrame([r.__dict__ for r in inventory_records])
    
    if '_sa_instance_state' in df_inventory.columns:
        df_inventory.drop('_sa_instance_state', axis=1, inplace=True)
    
    # If no data found, return default structure
    if df_inventory.empty:
        return _get_default_impact_data()
    
    # Calculate summary metrics
    summary_data = _calculate_summary_metrics(df_inventory, db, filters)
    
    # Get chart data
    last_7_days_data = _get_last_7_days_data(db, filters)
    monthly_store_data = _get_monthly_store_data(db, filters)
    
    # Get shrink report data
    shrink_report_data = _get_shrink_report_data(db, filters)
    
    return {
        "summary": summary_data,
        "last7DaysLossMitigation": last_7_days_data,
        "monthlyLossMitigationPerStore": monthly_store_data,
        "weeklyShrinkReport": shrink_report_data
    }

def _calculate_summary_metrics(df: pd.DataFrame, db: Session, filters: ImpactTrackerFilterParams) -> Dict:
    """Calculate summary metrics from inventory data"""
    
    # Calculate loss mitigation values based on inventory shrinkage prevention
    total_received = df['Actual_Quantity_Received'].fillna(0).sum()
    total_damaged = df['Number_Damaged_Units'].fillna(0).sum()
    total_expired = df['Number_Expired_Units'].fillna(0).sum()
    total_dump = df['Number_Dump_Units'].fillna(0).sum()
    
    # Estimate loss mitigation (prevented loss)
    avg_unit_cost = 25  # Estimated average unit cost
    todays_loss_mitigation = (total_damaged + total_expired + total_dump) * avg_unit_cost
    
    # For demo purposes, calculate MTD and YTD as multiples
    month_to_date = todays_loss_mitigation * 15  # Assuming 15 days in month
    year_to_date = todays_loss_mitigation * 180   # Assuming 180 days in year
    
    # Calculate alerts and other metrics
    shrinkage_alerts = len(df[df['Inventory_Status'].isin(['Critical - Expiring Soon', 'Expiry Approaching'])])
    
    return {
        "todays_loss_mitigation": int(todays_loss_mitigation),
        "todays_loss_mitigation_comparison": {
            "percentage": 4.8,
            "trend_direction": "up", 
            "compare_to": "LD"
        },
        "month_to_date_loss_mitigation": int(month_to_date),
        "month_to_date_loss_mitigation_comparison": {
            "percentage": 3.2,
            "trend_direction": "up",
            "compare_to": "LM"
        },
        "year_to_date_loss_mitigation": int(year_to_date),
        "year_to_date_loss_mitigation_comparison": {
            "percentage": 1.1,
            "trend_direction": "down", 
            "compare_to": "LY"
        },
        "shrinkage_alerts_triggered": shrinkage_alerts,
        "avg_time_for_resolution": "NA",
        "incident_frequency": 2
    }

def _get_last_7_days_data(db: Session, filters: ImpactTrackerFilterParams) -> List[Dict]:
    """Get last 7 days loss mitigation data"""
    
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)
    
    # Query data for last 7 days
    query = db.query(Inventory).filter(
        func.date(Inventory.Received_Date).between(start_date, end_date)
    )
    
    # Apply region filter if specified
    if filters.region:
        query = query.filter(Inventory.Region_Historical == filters.region)
    
    records = query.all()
    df = pd.DataFrame([r.__dict__ for r in records])
    
    if df.empty:
        # Return sample data if no real data
        return [
            {"date": "01-Jul", "value": 9000},
            {"date": "02-Jul", "value": 5000},
            {"date": "03-Jul", "value": 10000},
            {"date": "04-Jul", "value": 6000},
            {"date": "05-Jul", "value": 8000},
            {"date": "06-Jul", "value": 2000},
            {"date": "07-Jul", "value": 4000}
        ]
    
    # Group by date and calculate loss mitigation
    df['date'] = pd.to_datetime(df['Received_Date']).dt.date
    daily_data = df.groupby('date').agg({
        'Number_Damaged_Units': 'sum',
        'Number_Expired_Units': 'sum', 
        'Number_Dump_Units': 'sum'
    }).reset_index()
    
    # Calculate loss mitigation per day
    avg_unit_cost = 25
    daily_data['loss_mitigation'] = (
        daily_data['Number_Damaged_Units'] + 
        daily_data['Number_Expired_Units'] + 
        daily_data['Number_Dump_Units']
    ) * avg_unit_cost
    
    # Format for frontend
    result = []
    for _, row in daily_data.iterrows():
        result.append({
            "date": row['date'].strftime("%d-%b"),
            "value": int(row['loss_mitigation'])
        })
    
    return result

def _get_monthly_store_data(db: Session, filters: ImpactTrackerFilterParams) -> List[Dict]:
    """Get monthly loss mitigation data by store"""
    
    # Query current month data
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    query = db.query(Inventory).filter(
        func.extract('month', Inventory.Received_Date) == current_month,
        func.extract('year', Inventory.Received_Date) == current_year
    )
    
    if filters.region:
        query = query.filter(Inventory.Region_Historical == filters.region)
    
    records = query.all()
    df = pd.DataFrame([r.__dict__ for r in records])
    
    if df.empty:
        # Return sample data based on region
        sample_data = {
            "North": [
                {"store": "2145-NY", "value": 5000},
                {"store": "5360-PA", "value": 4500},
                {"store": "8243-NY", "value": 4000},
                {"store": "3682-CT", "value": 3500},
                {"store": "3296-L", "value": 3000}
            ],
            "South": [
                {"store": "3421-TX", "value": 4200},
                {"store": "7810-FL", "value": 3700},
                {"store": "9210-GA", "value": 3200},
                {"store": "6621-AL", "value": 2500},
                {"store": "1198-TN", "value": 1800}
            ]
        }
        return sample_data.get(filters.region, sample_data["North"])
    
    # Group by store and calculate loss mitigation
    store_data = df.groupby('Store_ID').agg({
        'Number_Damaged_Units': 'sum',
        'Number_Expired_Units': 'sum',
        'Number_Dump_Units': 'sum'
    }).reset_index()
    
    # Calculate loss mitigation per store
    avg_unit_cost = 25
    store_data['loss_mitigation'] = (
        store_data['Number_Damaged_Units'] + 
        store_data['Number_Expired_Units'] + 
        store_data['Number_Dump_Units']
    ) * avg_unit_cost
    
    # Sort and take top 10
    store_data = store_data.sort_values('loss_mitigation', ascending=False).head(10)
    
    result = []
    for _, row in store_data.iterrows():
        result.append({
            "store": row['Store_ID'],
            "value": int(row['loss_mitigation'])
        })
    
    return result

def _get_shrink_report_data(db: Session, filters: ImpactTrackerFilterParams) -> List[Dict]:
    """Get weekly shrink report data"""
    
    # This would typically come from a dedicated shrink/incident tracking table
    # For now, return sample data based on region
    
    sample_data = {
        "North": [
            {
                "date": "01/07/25",
                "store": "Store #329",
                "shrinkageType": "Lower Sell Through Rate",
                "estimatedLoss": 2300,
                "rootCause": "Poor Product Assortment",
                "actionTaken": "Reallocation to a store with high Sell Through Rate",
                "impactScore": 4,
                "followUpDate": "15/07/25"
            },
            {
                "date": "02/07/25", 
                "store": "Store #593",
                "shrinkageType": "Product (Inventory) Returned by Customer",
                "estimatedLoss": 800,
                "rootCause": "Return by Customer due to poor packaging",
                "actionTaken": "Donate to a nearby Homeless Center",
                "impactScore": 3,
                "followUpDate": "10/07/25"
            }
        ],
        "South": [
            {
                "date": "01/07/25",
                "store": "Store #2001 - TX", 
                "shrinkageType": "Theft",
                "estimatedLoss": 1800,
                "rootCause": "Internal Theft",
                "actionTaken": "Employee terminated and legal action taken",
                "impactScore": 5,
                "followUpDate": "15/07/25"
            }
        ]
    }
    
    return sample_data.get(filters.region, sample_data["North"])

def _get_default_impact_data() -> Dict:
    """Return default data when no records found"""
    return {
        "summary": {
            "todays_loss_mitigation": 0,
            "todays_loss_mitigation_comparison": {"percentage": 0, "trend_direction": "neutral", "compare_to": "LD"},
            "month_to_date_loss_mitigation": 0,
            "month_to_date_loss_mitigation_comparison": {"percentage": 0, "trend_direction": "neutral", "compare_to": "LM"},
            "year_to_date_loss_mitigation": 0,
            "year_to_date_loss_mitigation_comparison": {"percentage": 0, "trend_direction": "neutral", "compare_to": "LY"},
            "shrinkage_alerts_triggered": 0,
            "avg_time_for_resolution": 0,
            "incident_frequency": 0
        },
        "last7DaysLossMitigation": [],
        "monthlyLossMitigationPerStore": [],
        "weeklyShrinkReport": []
    }