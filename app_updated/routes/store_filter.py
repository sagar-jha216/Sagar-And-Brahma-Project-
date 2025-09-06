from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.store_filter import get_all_store_ids

router = APIRouter()

@router.get("/stores/all-store-ids")
def fetch_all_store_ids(db: Session = Depends(get_db)):
    store_ids = get_all_store_ids(db)
    # Flatten the list of tuples into a simple list
    return [store_id[0] for store_id in store_ids]
