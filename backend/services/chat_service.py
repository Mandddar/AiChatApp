"""
Chat service — business logic for chat and message operations.

All database interactions for chats and messages are encapsulated here,
keeping the router layer thin and focused on HTTP concerns.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.chat import Chat
from models.message import Message
from schemas.chat import ChatCreate, MessageCreate
from core.config import settings
import google.generativeai as genai

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)


# ---------------------------------------------------------------------------
# Chat operations
# ---------------------------------------------------------------------------

def create_chat(db: Session, chat_in: ChatCreate, user_id: int) -> Chat:
    """Create a new chat conversation for the given user."""
    db_chat = Chat(
        title=chat_in.title,
        user_id=user_id,
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


def get_user_chats(db: Session, user_id: int) -> list[Chat]:
    """Return all chats belonging to the given user, newest first."""
    return (
        db.query(Chat)
        .filter(Chat.user_id == user_id)
        .order_by(Chat.updated_at.desc())
        .all()
    )


def get_chat_by_id(db: Session, chat_id: int) -> Chat | None:
    """Return a single chat by ID, or None."""
    return db.query(Chat).filter(Chat.id == chat_id).first()


def validate_chat_ownership(db: Session, chat_id: int, user_id: int) -> Chat:
    """
    Fetch a chat and verify it belongs to the requesting user.

    Raises:
        HTTPException 404 — if the chat does not exist.
        HTTPException 403 — if the chat belongs to a different user.
    """
    chat = get_chat_by_id(db, chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )
    if chat.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this chat",
        )
    return chat


# ---------------------------------------------------------------------------
# Message operations
# ---------------------------------------------------------------------------

def get_chat_messages(db: Session, chat_id: int) -> list[Message]:
    """Return all messages for a chat, ordered chronologically."""
    return (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.created_at.asc())
        .all()
    )


def create_message(db: Session, chat_id: int, message_in: MessageCreate, role: str = "user") -> Message:
    """
    Create a new message in the specified chat.

    Args:
        db: Database session.
        chat_id: The chat this message belongs to.
        message_in: Validated message data from the client.
        role: Either "user" or "assistant". Defaults to "user" for Phase 1.
    """
    db_message = Message(
        chat_id=chat_id,
        role=role,
        content=message_in.content,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def process_chat_message(db: Session, chat_id: int, message_in: MessageCreate) -> list[Message]:
    """
    Process an incoming user message, generate an AI response via Gemini,
    save both to the database, and return them.
    """
    # 1. Save the user message
    user_msg = create_message(db, chat_id, message_in, role="user")

    # 2. Get full conversation history
    history = get_chat_messages(db, chat_id)

    # 3. Format history for Gemini API (roles: 'user' or 'model')
    gemini_history = []
    # Exclude the very last message we just added from history, 
    # since we pass the latest message directly to the chat session or as the new prompt.
    # Actually, Gemini `generate_content` can take the entire conversation array if it ends with 'user'.
    for msg in history:
        gemini_role = "user" if msg.role == "user" else "model"
        gemini_history.append({"role": gemini_role, "parts": [{"text": msg.content}]})

    # 4. Generate AI response
    assistant_text = "I am not configured with an API key yet. Please add GEMINI_API_KEY to your .env file."
    if settings.GEMINI_API_KEY:
        try:
            model = genai.GenerativeModel("gemini-flash-latest")
            response = model.generate_content(gemini_history)
            assistant_text = response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            assistant_text = "Sorry, I encountered an error while trying to process your request."

    # 5. Save the assistant message
    ai_msg_data = MessageCreate(content=assistant_text)
    assistant_msg = create_message(db, chat_id, ai_msg_data, role="assistant")

    return [user_msg, assistant_msg]
