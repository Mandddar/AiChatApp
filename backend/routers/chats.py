"""
Chat router — API endpoints for chat and message operations.

All routes require JWT authentication and enforce per-user ownership.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from schemas.chat import (
    ChatCreate,
    ChatResponse,
    ChatDetailResponse,
    MessageCreate,
    MessageResponse,
)
from core.dependencies import get_current_user, get_db
from models.user import User
from services.chat_service import (
    create_chat,
    get_user_chats,
    validate_chat_ownership,
    get_chat_messages,
    process_chat_message,
)


router = APIRouter(
    prefix="/chats",
    tags=["Chats"],
)


# ---------------------------------------------------------------------------
# Chat endpoints
# ---------------------------------------------------------------------------

@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def create_new_chat(
    chat_in: ChatCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new chat conversation for the authenticated user."""
    return create_chat(db, chat_in, user_id=current_user.id)


@router.get("/", response_model=list[ChatResponse])
def list_my_chats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return all chats belonging to the authenticated user."""
    return get_user_chats(db, user_id=current_user.id)


@router.get("/{chat_id}", response_model=ChatDetailResponse)
def get_chat_detail(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return a single chat with all its messages (ownership-validated)."""
    chat = validate_chat_ownership(db, chat_id, user_id=current_user.id)
    return chat


# ---------------------------------------------------------------------------
# Message endpoints
# ---------------------------------------------------------------------------

@router.get("/{chat_id}/messages", response_model=list[MessageResponse])
def list_chat_messages(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return all messages for a given chat (ownership-validated)."""
    validate_chat_ownership(db, chat_id, user_id=current_user.id)
    return get_chat_messages(db, chat_id)


@router.post("/{chat_id}/messages", response_model=list[MessageResponse], status_code=status.HTTP_201_CREATED)
def send_message(
    chat_id: int,
    message_in: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Send a user message in the specified chat.
    Generates and returns an AI response along with the user's message.
    """
    validate_chat_ownership(db, chat_id, user_id=current_user.id)
    return process_chat_message(db, chat_id, message_in, user_id=current_user.id)
