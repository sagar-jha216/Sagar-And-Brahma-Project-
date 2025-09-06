# app/routes/inventory.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.inventory import Inventory, InventoryCreate
from app.database import get_db
from app.controllers.inventory import create_inventory, get_inventory_by_id

router = APIRouter()

@router.post("/", response_model=Inventory)
def create(inventory: InventoryCreate, db: Session = Depends(get_db)):
    return create_inventory(inventory, db)

@router.get("/{id}", response_model=Inventory)
def read(id: int, db: Session = Depends(get_db)):
    return get_inventory(id, db)
