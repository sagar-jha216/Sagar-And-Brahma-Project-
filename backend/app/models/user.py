# app/models/products.py
from sqlalchemy import Column, String
from app.database import Base

class User(Base):
    __tablename__ = "user"
    userName =Column(String,primary_key=True,index=True)
    hashed_password=Column(String,nullable=False)
    
