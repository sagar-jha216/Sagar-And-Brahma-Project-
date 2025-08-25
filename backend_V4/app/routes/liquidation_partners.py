# app/routes/liquidator.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.liquidation_partners import LiquidationPartner, LiquidatorCreate
from app.database import get_db
from app.controllers.liquidation_partners import create_liquidator, get_liquidator

router = APIRouter()

@router.post("/", response_model=LiquidationPartner)
def create(liquidator: LiquidatorCreate, db: Session = Depends(get_db)):
    return create_liquidator(liquidator, db)

@router.get("/{id}", response_model=LiquidationPartner)
def read(id: int, db: Session = Depends(get_db)):
    return get_liquidator(id, db)
