from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.auth import create_access_token

router = APIRouter()

# Dummy database
fake_users = {
    "admin": "password123",
    "user1": "pass1"
}

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest):
    """
    Authenticate the user and return a JWT token (valid for 2 minutes).
    """
    if request.username not in fake_users or fake_users[request.username] != request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_access_token({"sub": request.username})
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 120
    }