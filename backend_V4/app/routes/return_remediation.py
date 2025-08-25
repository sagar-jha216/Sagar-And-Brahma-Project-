# app/routes/return_remediation.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.return_remediation import ReturnRemediation, ReturnRemediationCreate
from app.database import get_db
from app.controllers.return_remediation import get_return_remediations_by_return_id, get_return_remediation_by_id

router = APIRouter()

@router.post("/", response_model=ReturnRemediation)
def create(rr: ReturnRemediationCreate, db: Session = Depends(get_db)):
    return create_return_remediation(rr, db)

@router.get("/{id}", response_model=ReturnRemediation)
def read(id: int, db: Session = Depends(get_db)):
    return get_return_remediation(id, db)
