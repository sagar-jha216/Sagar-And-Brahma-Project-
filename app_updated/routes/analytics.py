# Backend\app\routes\analytics.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.analytics import get_shrinkage_analytics
import logging
 
router = APIRouter()
logger = logging.getLogger(__name__)
 
@router.get("/retail-leader-board")
def get_retail_leader_board_data(db: Session = Depends(get_db)):
    """
    Get shrinkage percentages by category and in-transit loss rate
    for the Retail Leader Board dashboard
    """
    try:
        data = get_shrinkage_analytics(db)
        
        # Validate that we have expected categories
        expected_categories = ["Produce (Fresh)", "Dry Goods", "General Merchandise"]
        missing_categories = [cat for cat in expected_categories 
                            if cat not in data["shrinkage_by_category"]]
        
        if missing_categories:
            logger.warning(f"Missing categories in response: {missing_categories}")
        
        # Log the actual data for debugging
        logger.info(f"Shrinkage data calculated: {data}")
        
        response = {
            "shrinkage_by_category": data["shrinkage_by_category"],
            "in_transit_loss_rate": data["in_transit_loss_rate"],
            "benchmarking_source": "NRF",
            "data_freshness": "real-time",
            "categories_available": list(data["shrinkage_by_category"].keys())
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Error calculating retail leader board data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to calculate shrinkage data")