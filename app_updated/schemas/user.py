from pydantic import BaseModel
from typing import Optional

# Base schema shared across models
class UserBase(BaseModel):
    userName: str
    isAdmin: bool

# Schema for creating a user
class UserCreate(UserBase):
    password: str  # Plain password to be hashed before storing

# Schema for login
class UserLogin(BaseModel):
    userName: str
    password: str

# Schema for updating user
class UserUpdate(BaseModel):
    userName: Optional[str] = None
    password: Optional[str] = None
    isAdmin: Optional[bool] = None


# Schema for returning user data
class User(UserBase):
    id:int
    hashed_password: str

    class Config:
        orm_mode = True
