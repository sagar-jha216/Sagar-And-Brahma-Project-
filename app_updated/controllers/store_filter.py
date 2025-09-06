from sqlalchemy.orm import Session
import pandas as pd
from app.models.stores import Store

def get_all_store_ids(db: Session):
    return db.query(Store.Store_ID).all()

    
