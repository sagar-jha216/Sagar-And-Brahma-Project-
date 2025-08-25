# app/routes/return.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.returns import Return, ReturnCreate
from app.database import get_db
from app.controllers.returns import create_return, get_return_by_id

router = APIRouter()

@router.post("/", response_model=Return)
def create(return_data: ReturnCreate, db: Session = Depends(get_db)):
    return create_return(return_data, db)

@router.get("/{id}", response_model=Return)
def read(id: int, db: Session = Depends(get_db)):
    return get_return(id, db)
