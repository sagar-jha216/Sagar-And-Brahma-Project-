from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.liquidation_partners import LiquidationPartner as LiquidationPartnerModel
from app.schemas.liquidation_partners import LiquidatorCreate, LiquidatorUpdate

# 🔹 Create a new liquidator
def create_liquidator(liquidator: LiquidatorCreate, db: Session):
    db_liquidator = LiquidationPartnerModel(**liquidator.dict(by_alias=True))
    db.add(db_liquidator)
    db.commit()
    db.refresh(db_liquidator)
    return db_liquidator

# 🔹 Get liquidator by internal ID
def get_liquidator(id: int, db: Session):
    liquidator = db.query(LiquidationPartnerModel).filter(LiquidationPartnerModel.id == id).first()
    if not liquidator:
        raise HTTPException(status_code=404, detail="Liquidator not found")
    return liquidator

# 🔹 Get liquidator by Liquidator_ID
def get_liquidator_by_code(liquidator_code: str, db: Session):
    liquidator = db.query(LiquidationPartnerModel).filter(
        LiquidationPartnerModel.Liquidator_ID == liquidator_code
    ).first()
    if not liquidator:
        raise HTTPException(status_code=404, detail="Liquidator not found")
    return liquidator

# 🔹 Update liquidator by ID
def update_liquidator(id: int, liquidator_update: LiquidatorUpdate, db: Session):
    liquidator = db.query(LiquidationPartnerModel).filter(LiquidationPartnerModel.id == id).first()
    if not liquidator:
        raise HTTPException(status_code=404, detail="Liquidator not found")

    for key, value in liquidator_update.dict(exclude_unset=True, by_alias=True).items():
        setattr(liquidator, key, value)

    db.commit()
    db.refresh(liquidator)
    return liquidator

# 🔹 Delete liquidator by ID
def delete_liquidator(id: int, db: Session):
    liquidator = db.query(LiquidationPartnerModel).filter(LiquidationPartnerModel.id == id).first()
    if not liquidator:
        raise HTTPException(status_code=404, detail="Liquidator not found")

    db.delete(liquidator)
    db.commit()
    return {"detail": "Liquidator deleted successfully"}
