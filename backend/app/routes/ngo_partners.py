# app/routes/ngo_partner.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.ngo_partners import NGOPartner, NGOPartnerCreate
from app.database import get_db
from app.controllers.ngo_partners import create_ngo_partner, get_ngo_partner

router = APIRouter()

@router.post("/", response_model=NGOPartner)
def create(ngo: NGOPartnerCreate, db: Session = Depends(get_db)):
    return create_ngo_partner(ngo, db)

@router.get("/{id}", response_model=NGOPartner)
def read(id: int, db: Session = Depends(get_db)):
    return get_ngo_partner(id, db)
