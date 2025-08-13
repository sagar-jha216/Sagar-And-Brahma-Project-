from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./shrink_sense.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

# Pydantic Models
class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_admin: Optional[bool] = False

class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str]
    full_name: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class LoginResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None
    user: Optional[UserResponse] = None

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="ShrinkSense Authentication API",
    description="Authentication system for ShrinkSense application",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password Utilities
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# JWT Utilities
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Database Operations
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def update_last_login(db: Session, user: User):
    user.last_login = datetime.utcnow()
    db.commit()
    return user

# API Routes
@app.get("/")
async def root():
    return {"message": "ShrinkSense Authentication API", "status": "running"}

@app.post("/auth/login", response_model=LoginResponse)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return access token.
    Compatible with the existing frontend login form.
    """
    try:
        # Authenticate user
        user = authenticate_user(db, user_credentials.username, user_credentials.password)
        
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
        
        # Update last login
        update_last_login(db, user)
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        # Return successful response
        user_response = UserResponse.from_orm(user)
        return LoginResponse(
            success=True,
            message="Login successful",
            token=access_token,
            user=user_response
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    if user.email:
        db_user_email = get_user_by_email(db, user.email)
        if db_user_email:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
    
    # Create new user
    db_user = create_user(db, user)
    return UserResponse.from_orm(db_user)

@app.get("/auth/me", response_model=UserResponse)
async def get_current_user(username: str = Depends(verify_token), db: Session = Depends(get_db)):
    """Get current user information"""
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse.from_orm(user)

@app.post("/auth/logout")
async def logout():
    """Logout endpoint (token invalidation handled on frontend)"""
    return {"message": "Logged out successfully"}

@app.get("/auth/verify-token")
async def verify_user_token(username: str = Depends(verify_token)):
    """Verify if token is valid"""
    return {"valid": True, "username": username}

# Protected route example
@app.get("/protected")
async def protected_route(username: str = Depends(verify_token), db: Session = Depends(get_db)):
    """Example protected route"""
    user = get_user_by_username(db, username)
    return {"message": f"Hello {user.full_name or user.username}!", "user_id": user.id}

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)