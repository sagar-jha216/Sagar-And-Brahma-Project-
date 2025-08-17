"""
FastAPI dependencies for authentication and database
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.models.user import User
from app.utils.security import verify_token
from app.config import settings

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> str:
    """Get current authenticated user"""
    username = verify_token(credentials.credentials)
    
    # Check if session has timed out
    if check_session_timeout(db, username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired due to inactivity"
        )
    
    # Update user activity
    update_user_activity(db, username)
    return username


def check_session_timeout(db: Session, username: str) -> bool:
    """Check if user session has timed out"""
    user = db.query(User).filter(User.username == username).first()
    if not user or not user.last_activity:
        return True
    
    timeout_threshold = datetime.utcnow() - timedelta(minutes=settings.SESSION_TIMEOUT_MINUTES)
    return user.last_activity < timeout_threshold


def update_user_activity(db: Session, username: str):
    """Update user's last activity timestamp"""
    user = db.query(User).filter(User.username == username).first()
    if user:
        user.last_activity = datetime.utcnow()
        db.commit()


def get_current_active_user(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """Get current active user object"""
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return user


def get_current_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Get current admin user"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user