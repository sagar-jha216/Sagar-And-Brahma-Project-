# app/controllers/inventory.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.inventory import Inventory as InventoryModel
from app.schemas.inventory import InventoryCreate

def create_inventory(inventory: InventoryCreate, db: Session):
    db_inventory = InventoryModel(**inventory.dict())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def get_inventory_by_id(inventory_id: int, db: Session):
    inventory = db.query(InventoryModel).filter(InventoryModel.id == inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return inventory

def get_inventory_by_sku(sku_id: str, db: Session):
    inventory = db.query(InventoryModel).filter(InventoryModel.sku_id == sku_id).all()
    if not inventory:
        raise HTTPException(status_code=404, detail="No inventory found for this SKU")
    return inventory

def update_inventory(inventory_id: int, inventory_update: InventoryCreate, db: Session):
    inventory = db.query(InventoryModel).filter(InventoryModel.id == inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    
    for key, value in inventory_update.dict(exclude_unset=True).items():
        setattr(inventory, key, value)
    
    db.commit()
    db.refresh(inventory)
    return inventory

def delete_inventory(inventory_id: int, db: Session):
    inventory = db.query(InventoryModel).filter(InventoryModel.id == inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    
    db.delete(inventory)
    db.commit()
    return {"detail": "Inventory record deleted successfully"}
