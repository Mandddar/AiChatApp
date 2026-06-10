from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user import User
from schemas.user import UserCreate
from schemas.auth import Token
from core.security import verify_password, create_access_token
from services.user_service import get_user_by_username, get_user_by_email, create_user

def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(db, username=username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def register_new_user(db: Session, user_in: UserCreate) -> User:
    existing_user = get_user_by_username(db, username=user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    existing_email = get_user_by_email(db, email=user_in.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return create_user(db, user_in)
