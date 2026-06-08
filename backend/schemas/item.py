"""
Pydantic schemas for Item request/response validation.

Schemas are the contract between the API and the outside world.
They handle serialization, deserialization, and validation — the
domain model (models/item.py) stays clean of HTTP concerns.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


# ---------------------------------------------------------------------------
# Request schemas (what the client sends)
# ---------------------------------------------------------------------------

class ItemCreate(BaseModel):
    """Schema for creating a new Item."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Display name of the item",
        examples=["Wireless Mouse"],
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Optional longer description",
        examples=["Ergonomic wireless mouse with USB-C receiver"],
    )
    price: float = Field(
        ...,
        gt=0,
        description="Price in USD — must be greater than zero",
        examples=[29.99],
    )
    is_available: bool = Field(
        default=True,
        description="Whether the item is currently available for purchase",
    )


class ItemUpdate(BaseModel):
    """
    Schema for updating an existing Item.

    Every field is optional so the client can send a partial update
    (PATCH semantics).
    """

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        examples=["Updated Mouse Name"],
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        examples=["Updated description"],
    )
    price: float | None = Field(
        default=None,
        gt=0,
        examples=[34.99],
    )
    is_available: bool | None = Field(
        default=None,
    )


# ---------------------------------------------------------------------------
# Response schemas (what the API returns)
# ---------------------------------------------------------------------------

class ItemResponse(BaseModel):
    """Full Item representation returned to the client."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None
    price: float
    is_available: bool
    created_at: datetime
    updated_at: datetime


class ItemListResponse(BaseModel):
    """Wrapper for returning a list of items with metadata."""

    items: list[ItemResponse]
    total: int
