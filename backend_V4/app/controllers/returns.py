# app/controllers/returns.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.returns import Return as ReturnModel
from app.schemas.returns import ReturnCreate, ReturnUpdate

def create_return(return_data: ReturnCreate, db: Session):
    db_return = ReturnModel(**return_data.dict())
    db.add(db_return)
    db.commit()
    db.refresh(db_return)
    return db_return

def get_return_by_id(return_id: int, db: Session):
    return_record = db.query(ReturnModel).filter(ReturnModel.id == return_id).first()
    if not return_record:
        raise HTTPException(status_code=404, detail="Return record not found")
    return return_record

def get_returns_by_return_id(return_code: str, db: Session):
    returns = db.query(ReturnModel).filter(ReturnModel.return_id == return_code).all()
    if not returns:
        raise HTTPException(status_code=404, detail="No returns found for this return ID")
    return returns

def update_return(return_id: int, return_update: ReturnUpdate, db: Session):
    return_record = db.query(ReturnModel).filter(ReturnModel.id == return_id).first()
    if not return_record:
        raise HTTPException(status_code=404, detail="Return record not found")
    
    for key, value in return_update.dict(exclude_unset=True).items():
        setattr(return_record, key, value)
    
    db.commit()
    db.refresh(return_record)
    return return_record

def delete_return(return_id: int, db: Session):
    return_record = db.query(ReturnModel).filter(ReturnModel.id == return_id).first()
    if not return_record:
        raise HTTPException(status_code=404, detail="Return record not found")
    
    db.delete(return_record)
    db.commit()
    return {"detail": "Return record deleted successfully"}
