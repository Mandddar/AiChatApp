"""
Dependency injection providers.

FastAPI's Depends() system wires these into route handlers so
services are created once and shared across the request lifecycle.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError

from services.item_service import ItemService
from database.session import SessionLocal
from core.config import settings
from schemas.auth import TokenData
from models.user import User
from services.user_service import get_user_by_username

# ---------------------------------------------------------------------------
# Singleton service instances
#
# Because we use in-memory storage, we need a single ItemService
# instance that persists across requests. When we move to a real
# database, these can become request-scoped instead.
# ---------------------------------------------------------------------------

_item_service = ItemService()


def get_item_service() -> ItemService:
    """Provide the shared ItemService instance via FastAPI Depends."""
    return _item_service

# ---------------------------------------------------------------------------
# Database and Auth Dependencies
# ---------------------------------------------------------------------------

def get_db():
    """Dependency to provide a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

