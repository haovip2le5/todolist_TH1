from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import UserModel
from app.schemas.user import UserRegister, UserLogin, User, Token, TokenData
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserModel:
    """Dependency to get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = AuthService.verify_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception
    
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise credentials_exception
    
    user = AuthService.get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    
    return user


def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserModel:
    """Dependency to get optional current user - returns default user if no token (for testing)"""
    # If no token provided, use default user_id = 1
    if token is None:
        return AuthService.get_user_by_id(db, 1)
    
    payload = AuthService.verify_token(token)
    if payload is None:
        # Token invalid, use default user
        return AuthService.get_user_by_id(db, 1)
    
    user_id_str = payload.get("sub")
    if user_id_str is None:
        return AuthService.get_user_by_id(db, 1)
    
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        return AuthService.get_user_by_id(db, 1)
    
    user = AuthService.get_user_by_id(db, user_id)
    if user is None:
        return AuthService.get_user_by_id(db, 1)
    
    return user


@router.post("/register", response_model=User)
def register(user: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_user = AuthService.register_user(db, user.email, user.password)
    return new_user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login user and return JWT token (supports OAuth2 form data)"""
    # form_data.username = email, form_data.password = password
    db_user = AuthService.login_user(db, form_data.username, form_data.password)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    access_token = AuthService.create_access_token(db_user.id, db_user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
def get_me(current_user: UserModel = Depends(get_current_user)):
    """Get current authenticated user info"""
    return current_user



