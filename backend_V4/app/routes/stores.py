# app/routes/store.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.stores import Store, StoreCreate
from app.database import get_db
from app.controllers.stores import create_store, get_store

router = APIRouter()

@router.post("/", response_model=Store)
def create(store: StoreCreate, db: Session = Depends(get_db)):
    return create_store(store, db)

@router.get("/{id}", response_model=Store)
def read(id: int, db: Session = Depends(get_db)):
    return get_store(id, db)
