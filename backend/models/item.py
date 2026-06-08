"""
Item domain model.

This represents the internal data structure for an Item.
Models live in this layer and are independent of HTTP or database concerns.
"""

from datetime import datetime
from uuid import UUID


class Item:
    """Domain entity representing an Item in the system."""

    def __init__(
        self,
        id: UUID,
        name: str,
        description: str | None,
        price: float,
        is_available: bool,
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.is_available = is_available
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"<Item id={self.id} name={self.name!r}>"
