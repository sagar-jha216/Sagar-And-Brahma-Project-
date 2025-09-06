from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.remediation_controller import get_remediation_recommendations
from typing import Optional, List
from datetime import date
import logging
from pydantic import BaseModel, Field

router = APIRouter()
logger = logging.getLogger(__name__)

class RemediationFilterParams(BaseModel):
    Region_Historical: Optional[str] = Field(None, alias="Region_Historical")
    Store_ID: Optional[List[str]] = Field(None, alias="Store_ID")
    Store_Channel: Optional[List[str]] = Field(None, alias="Store_Channel")
    Received_Date: Optional[date] = Field(None, alias="Received_Date")

    class Config:
        allow_population_by_field_name = True

class RemediationResponse(BaseModel):
    recommendation_rank: int
    recommended_action: str
    action_quantity: int
    target_name: Optional[str]
    #target_store_name: Optional[str]
    gross_margin_pct: float
    net_loss_mitigation: float
    #expected_recovery: float
    #tax_benefit_amount: float

class IssueResponse(BaseModel):
    issue_id: str
    #issue_type: str
    #sku_id: str
    product_name: str
    #store_id: str
    store_name: Optional[str]
    quantity_on_hand: int
    shelf_life_remaining: int
    sell_through_rate_per_day: float
    unit_cost: float
    #risk_level: str
    #category: str
    potential_loss_mitigation: float
    remediations: List[RemediationResponse]

class RemediationRecommendationsResponse(BaseModel):
    issues: List[IssueResponse]
    total_issues: int
    filters_applied: dict

@router.post("/remediation-recommendations", response_model=RemediationRecommendationsResponse)
def get_remediation_recommendations_endpoint(
    filters: RemediationFilterParams, 
    db: Session = Depends(get_db)
):
    """
    Get remediation recommendations grouped by issue_id.
    Each issue contains the inventory details and multiple remediation options ranked by preference.
    """
    try:
        result = get_remediation_recommendations(filters, db)
        return result
    except Exception as e:
        logger.error(f"Error getting remediation recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get remediation recommendations")

@router.get("/remediation-recommendations/issue/{issue_id}")
def get_single_issue_recommendations(
    issue_id: str,
    db: Session = Depends(get_db)
):
    """
    Get remediation recommendations for a specific issue_id
    """
    try:
        # Create empty filters to get all data, then filter by issue_id
        from app.controllers.remediation_controller import apply_remediation_filters
        from app.models.inventory import Inventory
        from app.models.remediation_recommendations import RemediationRecommendation
        from app.models.stores import Store
        import pandas as pd
        
        # Query data
        recommendation_records = db.query(RemediationRecommendation).filter(
            RemediationRecommendation.issue_id == issue_id
        ).all()
        
        if not recommendation_records:
            raise HTTPException(status_code=404, detail=f"Issue {issue_id} not found")
        
        store_records = db.query(Store).all()
        
        # Convert to DataFrames
        df_recommendations = pd.DataFrame([r.__dict__ for r in recommendation_records])
        df_stores = pd.DataFrame([r.__dict__ for r in store_records])
        
        # Remove SQLAlchemy internal state columns
        for df in [df_recommendations, df_stores]:
            if '_sa_instance_state' in df.columns:
                df.pop('_sa_instance_state')
        
        # Get the first record for issue-level information
        first_rec = df_recommendations.iloc[0]
        
        # Calculate potential loss mitigation
        potential_loss_mitigation = df_recommendations['net_loss_mitigation'].fillna(0).sum()
        
        # Prepare remediation recommendations
        remediations = []
        for _, rec in df_recommendations.iterrows():
            # Get store name if available
            store_name = None
            if rec['target_name'] and rec['target_name'] in df_stores['Store_ID'].values:
                store_row = df_stores[df_stores['Store_ID'] == rec['target_name']]
                if not store_row.empty:
                    store_name = store_row.iloc[0]['Store_Name']
            
            remediations.append({
                "recommendation_rank": int(rec['recommendation_rank']) if pd.notna(rec['recommendation_rank']) else 1,
                "recommended_action": rec['recommended_action'],
                "action_quantity": int(rec['action_quantity']) if pd.notna(rec['action_quantity']) else 0,
                "target_name": rec['target_name'],
                "target_store_name": store_name,
                "gross_margin_pct": round(rec['gross_margin_pct'], 2) if pd.notna(rec['gross_margin_pct']) else 0,
                "net_loss_mitigation": round(rec['net_loss_mitigation'], 2) if pd.notna(rec['net_loss_mitigation']) else 0,
                "expected_recovery": round(rec['expected_recovery'], 2) if pd.notna(rec['expected_recovery']) else 0,
                "tax_benefit_amount": round(rec['tax_benefit_amount'], 2) if pd.notna(rec['tax_benefit_amount']) else 0
            })
        
        # Sort remediations by recommendation rank
        remediations.sort(key=lambda x: x['recommendation_rank'])
        
        # Determine issue type
        issue_type = "Lower Sell-Through Rate"
        if first_rec['risk_level'] == "CRITICAL":
            issue_type = "Critical Expiry"
        elif first_rec['risk_level'] == "VERY_HIGH":
            issue_type = "High Risk Inventory"
        elif first_rec['inventory_age_days'] > 60:
            issue_type = "Seasonal Overstock"
        
        # Get store name for the issue
        issue_store_name = None
        if first_rec['store_id'] in df_stores['Store_ID'].values:
            store_row = df_stores[df_stores['Store_ID'] == first_rec['store_id']]
            if not store_row.empty:
                issue_store_name = store_row.iloc[0]['Store_Name']
        
        return {
            "issue_id": issue_id,
            "issue_type": issue_type,
            "sku_id": first_rec['sku_id'],
            "product_name": first_rec['product_name'],
            "store_id": first_rec['store_id'],
            "store_name": issue_store_name,
            "quantity_on_hand": int(first_rec['quantity_on_hand']) if pd.notna(first_rec['quantity_on_hand']) else 0,
            "shelf_life_remaining": int(first_rec['shelf_life_remaining']) if pd.notna(first_rec['shelf_life_remaining']) else 0,
            "sell_through_rate_per_day": round(first_rec['Sell_Through_Rate_Per_Day'], 2) if pd.notna(first_rec['Sell_Through_Rate_Per_Day']) else 0,
            "unit_cost": round(first_rec['unit_cost'], 2) if pd.notna(first_rec['unit_cost']) else 0,
            "risk_level": first_rec['risk_level'],
            "category": first_rec['category'],
            "potential_loss_mitigation": round(potential_loss_mitigation, 2),
            "remediations": remediations
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting issue {issue_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get issue {issue_id}")