from sqlalchemy import Column, String, Boolean, Integer
from app.database import Base

class User(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True)
    userName = Column(String, unique=True, index=True) 
    hashed_password = Column(String, nullable=False)
    isAdmin = Column(Boolean, default=False)  # Default value set to False



