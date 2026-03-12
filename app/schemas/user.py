from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserRegister(BaseModel):
    """Schema đăng ký user"""
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Schema đăng nhập user"""
    email: EmailStr
    password: str


class User(BaseModel):
    """Schema user"""
    id: int
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema token"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema token data"""
    user_id: int
    email: str
