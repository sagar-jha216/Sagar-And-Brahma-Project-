# app/routes/remediation_recommendation.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.remediation_recommendations import RemediationRecommendation, RemediationRecommendationCreate
from app.database import get_db
from app.controllers.remediation_recommendations import create_remediation_recommendation, get_remediation_recommendation

router = APIRouter()

@router.post("/", response_model=RemediationRecommendation)
def create(rr: RemediationRecommendationCreate, db: Session = Depends(get_db)):
    return create_remediation_recommendation(rr, db)

@router.get("/{id}", response_model=RemediationRecommendation)
def read(id: int, db: Session = Depends(get_db)):
    return get_remediation_recommendation(id, db)
