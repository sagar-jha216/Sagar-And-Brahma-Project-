from fastapi import APIRouter, Depends, HTTPException, status, Cookie, Response
from sqlalchemy.orm import Session
from typing import List
from app.utils.auth import create_access_token
from app.schemas.user import User, UserCreate, UserUpdate, UserLogin
from app.database import get_db
from app.middleware.auth_middleware import verify_admin


from app.controllers.user import (
    create_user,
    get_user,
    get_all_users,
    update_user,
    delete_user,
    authenticate_user,
)

router = APIRouter()

# ✅ Create user
@router.post("/", response_model=User)
def create(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)

# Login
@router.post("/login", response_model=User)
def login(credentials: UserLogin,response: Response, db: Session = Depends(get_db)):
    user = authenticate_user(credentials.userName, credentials.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
     # Create JWT token
    token = create_access_token(data={
        "sub": user.userName,
        "isAdmin": user.isAdmin
        })

    # Set HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="Lax",
        max_age=900,
        path="/",
    )
#     response.set_cookie(
#     key="access_token",
#     value=token,
#     httponly=True,
#     secure=False,         # Use True only with HTTPS
#     samesite="None",      # Required for cross-origin cookies
#     path="/",             # Ensures it's sent with all routes
#     domain="localhost"    # Must match frontend domain
# )

    return user

# Get all users
@router.get("/", response_model=List[User])
def read_all(db: Session = Depends(get_db),current_admin: dict = Depends(verify_admin)):
    return get_all_users(db)

@router.get("/me")
def read_current_user(current_user: dict = Depends(verify_admin)):
    return {"userName": current_user} 
    
# Get user by id
@router.get("/{id}", response_model=User)
def read(id: str, db: Session = Depends(get_db),current_admin: dict = Depends(verify_admin)):
    return get_user(id, db)

# Update user
@router.put("/{id}", response_model=User)
def update(id: str, user_update: UserUpdate, db: Session = Depends(get_db),current_admin: dict = Depends(verify_admin)):
    return update_user(id, user_update, db)

# Delete user
@router.delete("/{id}")
def delete(id: str, db: Session = Depends(get_db),current_admin: dict = Depends(verify_admin)):
    return delete_user(id, db)


