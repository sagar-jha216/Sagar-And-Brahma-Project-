from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.return_remediation import ReturnRemediation as RemediationModel
from app.schemas.return_remediation import (
    ReturnRemediationCreate,
    ReturnRemediationUpdate
)

def create_return_remediation(remediation: ReturnRemediationCreate, db: Session):
    # Use by_alias=True to match schema aliases with model field names
    db_remediation = RemediationModel(**remediation.dict(by_alias=True))
    db.add(db_remediation)
    db.commit()
    db.refresh(db_remediation)
    return db_remediation

def get_return_remediation_by_id(remediation_id: int, db: Session):
    remediation = db.query(RemediationModel).filter(RemediationModel.id == remediation_id).first()
    if not remediation:
        raise HTTPException(status_code=404, detail="Return remediation not found")
    return remediation

def get_return_remediations_by_return_id(return_id: str, db: Session):
    remediations = db.query(RemediationModel).filter(RemediationModel.return_id == return_id).all()
    if not remediations:
        raise HTTPException(status_code=404, detail="No remediations found for this return ID")
    return remediations

def update_return_remediation(remediation_id: int, remediation_update: ReturnRemediationUpdate, db: Session):
    remediation = db.query(RemediationModel).filter(RemediationModel.id == remediation_id).first()
    if not remediation:
        raise HTTPException(status_code=404, detail="Return remediation not found")
    
    # Use by_alias=True to ensure correct field names
    for key, value in remediation_update.dict(exclude_unset=True, by_alias=True).items():
        setattr(remediation, key, value)
    
    db.commit()
    db.refresh(remediation)
    return remediation

def delete_return_remediation(remediation_id: int, db: Session):
    remediation = db.query(RemediationModel).filter(RemediationModel.id == remediation_id).first()
    if not remediation:
        raise HTTPException(status_code=404, detail="Return remediation not found")
    
    db.delete(remediation)
    db.commit()
    return {"detail": "Return remediation deleted successfully"}
