"""
Authentication controller for ShrinkSense application
"""

from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import jwt

from app.database import get_db, User, hash_password, verify_password, update_user_activity
from app.middleware.auth import verify_token
from app.config import get_settings

settings = get_settings()
router = APIRouter()
security = HTTPBearer()

# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None
    user: Optional[dict] = None

class TokenData(BaseModel):
    username: Optional[str] = None

class UserCreateRequest(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_admin: bool = False

class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str]
    full_name: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: datetime
    last_login: Optional[datetime]

# JWT functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def check_session_timeout(db: Session, username: str) -> bool:
    user = db.query(User).filter(User.username == username).first()
    if not user or not user.last_activity:
        return True
    
    timeout_threshold = datetime.utcnow() - timedelta(minutes=settings.SESSION_TIMEOUT_MINUTES)
    return user.last_activity < timeout_threshold

# Routes
@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token"""
    user = authenticate_user(db, login_data.username, login_data.password)
    
    if not user:
        return LoginResponse(
            success=False,
            message="Invalid credentials. Please try again."
        )
    
    if not user.is_active:
        return LoginResponse(
            success=False,
            message="Account is inactive. Please contact administrator."
        )
    
    # Update login timestamps
    user.last_login = datetime.utcnow()
    user.last_activity = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return LoginResponse(
        success=True,
        message="Login successful",
        token=access_token,
        user={
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "is_admin": user.is_admin
        }
    )

@router.post("/logout")
async def logout():
    """Logout endpoint"""
    return {"success": True, "message": "Logged out successfully"}

@router.get("/verify")
async def verify_session(username: str = Depends(verify_token), db: Session = Depends(get_db)):
    """Verify token and check session timeout"""
    if check_session_timeout(db, username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired due to inactivity"
        )
    
    update_user_activity(db, username)
    user = get_user_by_username(db, username)
    
    return {
        "valid": True,
        "username": username,
        "user": {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "is_admin": user.is_admin
        }
    }

@router.post("/refresh-activity")
async def refresh_activity(username: str = Depends(verify_token), db: Session = Depends(get_db)):
    """Refresh user activity timestamp"""
    update_user_activity(db, username)
    return {"success": True, "message": "Activity refreshed"}

@router.get("/me", response_model=UserResponse)
async def get_current_user(username: str = Depends(verify_token), db: Session = Depends(get_db)):
    """Get current user information"""
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        is_admin=user.is_admin,
        created_at=user.created_at,
        last_login=user.last_login
    )

@router.post("/create-user", response_model=UserResponse)
async def create_user(
    user_data: UserCreateRequest,
    current_user: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Create new user (admin only)"""
    admin_user = get_user_by_username(db, current_user)
    if not admin_user or not admin_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Check if user already exists
    existing_user = get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create new user
    new_user = User(
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        email=user_data.email,
        full_name=user_data.full_name,
        is_admin=user_data.is_admin
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        full_name=new_user.full_name,
        is_active=new_user.is_active,
        is_admin=new_user.is_admin,
        created_at=new_user.created_at,
        last_login=new_user.last_login
    )