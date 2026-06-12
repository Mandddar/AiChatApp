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


def process_chat_message(db: Session, chat_id: int, message_in: MessageCreate, user_id: int) -> list[Message]:
    """
    Process an incoming user message, generate an AI response via Gemini,
    save both to the database, and return them.

    If the user has uploaded documents, relevant chunks are retrieved
    from the vector store and injected into the system prompt.
    """
    # 1. Save the user message
    user_msg = create_message(db, chat_id, message_in, role="user")

    # 2. Get full conversation history
    history = get_chat_messages(db, chat_id)

    # 3. Format history for Gemini API (roles: 'user' or 'model')
    gemini_history = []
    for msg in history:
        gemini_role = "user" if msg.role == "user" else "model"
        gemini_history.append({"role": gemini_role, "parts": [{"text": msg.content}]})

    # Release the database transaction before we make long network calls 
    # to prevent Neon Serverless Postgres from dropping the idle connection.
    db.commit()

    # 4. Retrieve relevant document context (RAG)
    context_text = ""
    try:
        from services.rag_service import search_documents
        relevant_chunks = search_documents(message_in.content, user_id, n_results=5)
        if relevant_chunks:
            context_text = "\n\n---\n\n".join(relevant_chunks)
    except Exception as e:
        print(f"RAG search error (non-fatal): {e}")

    # 5. Build system instruction with optional document context
    base_instruction = (
        "Your name is Aurora. You are a helpful, friendly, and highly intelligent "
        "AI assistant created for this application. Never say you are developed by Google."
    )
    if context_text:
        base_instruction += (
            "\n\nThe user has uploaded documents. Below are relevant excerpts from those "
            "documents that may help you answer the user's question. Use this context when "
            "relevant, but don't force it if the user's question is unrelated.\n\n"
            f"--- DOCUMENT CONTEXT ---\n{context_text}\n--- END CONTEXT ---"
        )

    # 6. Generate AI response
    assistant_text = "I am not configured with an API key yet. Please add GEMINI_API_KEY to your .env file."
    if settings.GEMINI_API_KEY:
        try:
            model = genai.GenerativeModel(
                "gemini-flash-latest",
                system_instruction=base_instruction,
            )
            response = model.generate_content(gemini_history)
            assistant_text = response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            assistant_text = "Sorry, I encountered an error while trying to process your request."

    # 7. Save the assistant message
    ai_msg_data = MessageCreate(content=assistant_text)
    assistant_msg = create_message(db, chat_id, ai_msg_data, role="assistant")

    return [user_msg, assistant_msg]