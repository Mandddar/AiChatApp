"""
Pydantic schemas for Document request/response validation.
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    """Full Document representation returned to the client."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    original_name: str
    file_size: int
    chunk_count: int
    status: str
    user_id: int
    created_at: datetime
