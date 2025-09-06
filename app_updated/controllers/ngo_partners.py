# app/controllers/ngo_partner.py
from sqlalchemy.orm import Session
from app.models.ngo_partners import NGOPartner as NGOPartnerModel
from app.schemas.ngo_partners import NGOPartnerCreate

def create_ngo_partner(ngo: NGOPartnerCreate, db: Session):
    db_ngo = NGOPartnerModel(**ngo.dict())
    db.add(db_ngo)
    db.commit()
    db.refresh(db_ngo)
    return db_ngo

def get_ngo_partner(id: int, db: Session):
    return db.query(NGOPartnerModel).filter(NGOPartnerModel.id == id).first()
