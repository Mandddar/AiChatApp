"""
Item service — business logic layer.

All Item-related business rules live here. The service operates on
domain models and schemas, keeping routers thin. Uses in-memory
storage (a dict) that will be swapped for a real database later.
"""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import HTTPException, status

from models.item import Item
from schemas.item import ItemCreate, ItemUpdate, ItemResponse, ItemListResponse


class ItemService:
    """
    Handles all CRUD operations for Items.

    Storage is an in-memory dict keyed by UUID. Because this is a
    class instance, it can later be replaced with a repository that
    talks to a real database — no router changes needed.
    """

    def __init__(self) -> None:
        # In-memory store: UUID -> Item domain object
        self._store: dict[UUID, Item] = {}

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------
    async def create_item(self, payload: ItemCreate) -> ItemResponse:
        """Create a new Item and return its full representation."""

        now = datetime.now(timezone.utc)
        item = Item(
            id=uuid4(),
            name=payload.name,
            description=payload.description,
            price=payload.price,
            is_available=payload.is_available,
            created_at=now,
            updated_at=now,
        )
        self._store[item.id] = item
        return self._to_response(item)

    # ------------------------------------------------------------------
    # READ (single)
    # ------------------------------------------------------------------
    async def get_item(self, item_id: UUID) -> ItemResponse:
        """Retrieve a single Item by its UUID."""

        item = self._store.get(item_id)
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id '{item_id}' not found",
            )
        return self._to_response(item)

    # ------------------------------------------------------------------
    # READ (list)
    # ------------------------------------------------------------------
    async def list_items(self) -> ItemListResponse:
        """Return all Items currently in the store."""

        items = list(self._store.values())
        return ItemListResponse(
            items=[self._to_response(i) for i in items],
            total=len(items),
        )

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------
    async def update_item(
        self, item_id: UUID, payload: ItemUpdate
    ) -> ItemResponse:
        """
        Partially update an existing Item.

        Only fields explicitly provided in the payload are updated.
        """

        item = self._store.get(item_id)
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id '{item_id}' not found",
            )

        # Apply only the fields the client actually sent
        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)

        item.updated_at = datetime.now(timezone.utc)
        return self._to_response(item)

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    async def delete_item(self, item_id: UUID) -> ItemResponse:
        """Remove an Item from the store and return its last state."""

        item = self._store.pop(item_id, None)
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id '{item_id}' not found",
            )
        return self._to_response(item)

    # ------------------------------------------------------------------
    # Internal helper
    # ------------------------------------------------------------------
    @staticmethod
    def _to_response(item: Item) -> ItemResponse:
        """Convert a domain Item to its API response schema."""

        return ItemResponse(
            id=item.id,
            name=item.name,
            description=item.description,
            price=item.price,
            is_available=item.is_available,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )
