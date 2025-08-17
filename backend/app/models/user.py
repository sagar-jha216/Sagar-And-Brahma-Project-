"""
User authentication model for ShrinkSense
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Session
from datetime import datetime
import bcrypt
import logging

from .base import Base, engine

logger = logging.getLogger(__name__)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    last_activity = Column(DateTime, default=datetime.utcnow)

# Authentication utilities
def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_default_admin():
    """Create default admin user if not exists"""
    with Session(engine) as session:
        admin = session.query(User).filter(User.username == "admin").first()
        if not admin:
            admin_user = User(
                username="admin",
                hashed_password=hash_password("admin"),
                email="admin@shrinksense.com",
                full_name="System Administrator",
                is_admin=True
            )
            session.add(admin_user)
            session.commit()
            logger.info("Default admin user created")

def update_user_activity(db: Session, username: str):
    """Update user last activity timestamp"""
    user = db.query(User).filter(User.username == username).first()
    if user:
        user.last_activity = datetime.utcnow()
        db.commit()