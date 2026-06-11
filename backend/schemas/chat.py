"""
Pydantic schemas for Chat and Message request/response validation.

These schemas define the API contract for all chat-related endpoints.
"""

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


# ---------------------------------------------------------------------------
# Message schemas
# ---------------------------------------------------------------------------

class MessageCreate(BaseModel):
    """Schema for creating a new message in a chat."""

    content: str = Field(
        ...,
        min_length=1,
        description="The text content of the message",
        examples=["Hello, how can you help me today?"],
    )


class MessageResponse(BaseModel):
    """Full Message representation returned to the client."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    chat_id: int
    role: str
    content: str
    created_at: datetime


# ---------------------------------------------------------------------------
# Chat schemas
# ---------------------------------------------------------------------------

class ChatCreate(BaseModel):
    """Schema for creating a new chat."""

    title: str = Field(
        default="New Chat",
        min_length=1,
        max_length=255,
        description="Title of the chat conversation",
        examples=["Python Help"],
    )


class ChatResponse(BaseModel):
    """Full Chat representation returned to the client."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    user_id: int
    created_at: datetime
    updated_at: datetime


class ChatDetailResponse(ChatResponse):
    """Chat with its messages included."""

    messages: list[MessageResponse] = []
