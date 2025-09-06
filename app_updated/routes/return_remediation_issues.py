from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.return_remediation_controller import (
    get_return_issues_with_remediations,
    # get_single_issue_details
)
from typing import Optional, List
from datetime import date
import logging
from pydantic import BaseModel, Field

router = APIRouter()
logger = logging.getLogger(__name__)


class ReturnRemediationFilterParams(BaseModel):
    Region_Historical: Optional[str] = Field(None, alias="Region_Historical")
    Store_ID: Optional[List[str]] = Field(None, alias="Store_ID")
    Store_Channel: Optional[List[str]] = Field(None, alias="Store_Channel")
    Received_Date: Optional[date] = Field(None, alias="Received_Date")

    class Config:
        populate_by_name = True


@router.post("/return-issues")
def get_return_issues(
    filters: ReturnRemediationFilterParams, 
    db: Session = Depends(get_db)
):
    """
    Get all return issues with their remediation options.
    Returns issues grouped by issue_id with potential loss mitigation calculations.
    """
    try:
        logger.info(f"Fetching return issues with filters: {filters.dict()}")
        result = get_return_issues_with_remediations(filters, db)
        
        logger.info(f"Successfully fetched {result['total_issues']} return issues")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching return issues: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to retrieve return issues: {str(e)}"
        )


# @router.get("/return-issues/{issue_id}")
# def get_issue_details(
#     issue_id: str = Path(..., description="The issue ID to retrieve details for"),
#     db: Session = Depends(get_db)
# ):
#     """
#     Get detailed information for a specific return issue including all remediation options.
#     """
#     try:
#         logger.info(f"Fetching details for issue: {issue_id}")
#         result = get_single_issue_details(issue_id, db)
        
#         if not result:
#             logger.warning(f"Issue with ID '{issue_id}' not found")
#             raise HTTPException(
#                 status_code=404, 
#                 detail=f"Issue with ID '{issue_id}' not found"
#             )
        
#         logger.info(f"Successfully fetched details for issue: {issue_id}")
#         return result
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Error fetching issue details for {issue_id}: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(
#             status_code=500, 
#             detail=f"Failed to retrieve issue details: {str(e)}"
#         )