from sqlalchemy.orm import Session
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext
from fastapi import Cookie, HTTPException, status
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



# Create user
def create_user(user: UserCreate, db: Session):
    existing_user = db.query(UserModel).filter(UserModel.userName == user.userName).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    hashed_pw = hash_password(user.password)
    db_user = UserModel(
        userName=user.userName,
        hashed_password=hashed_pw,
        isAdmin=user.isAdmin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Authenticate user
def authenticate_user(userName: str, password: str, db: Session):
    user = db.query(UserModel).filter(UserModel.userName == userName).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None

# Get all users
def get_all_users(db: Session):
    return db.query(UserModel).all()

# Get user by username
def get_user(id: str, db: Session):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if not user:
        raise Exception("User not found")
    return user

# Update user
def update_user(id: str, user_update: UserUpdate, db: Session):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if not user:
        raise Exception("User not found")

      # Check for unique username
    if user_update.userName and user_update.userName != user.userName:
        existing_user = db.query(UserModel).filter(UserModel.userName == user_update.userName).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        user.userName = user_update.userName


    if user_update.password:
        user.hashed_password = hash_password(user_update.password)
    if user_update.isAdmin is not None:
        user.isAdmin = user_update.isAdmin

    db.commit()
    db.refresh(user)
    return user

# Delete user
def delete_user(id: str, db: Session):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if not user:
        raise Exception("User not found")

    db.delete(user)
    db.commit()
    return {"message": f"User '{user.userName}' deleted successfully"}
