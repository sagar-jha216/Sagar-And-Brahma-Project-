from sqlalchemy.orm import Session
from app.models.stores import Store as StoreModel
from app.schemas.stores import StoreCreate

def create_store(store: StoreCreate, db: Session):
    db_store = StoreModel(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

def get_store(id: int, db: Session):
    return db.query(StoreModel).filter(StoreModel.id == id).first()