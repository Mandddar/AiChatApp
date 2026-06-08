"""
Item router — full CRUD endpoints for the Item resource.

Routes are intentionally thin: they receive the HTTP request, delegate
to the service layer, and return the response. No business logic here.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, status

from core.dependencies import get_item_service
from schemas.item import (
    ItemCreate,
    ItemUpdate,
    ItemResponse,
    ItemListResponse,
)
from services.item_service import ItemService

router = APIRouter(
    prefix="/items",
    tags=["Items"],
)


# ---------------------------------------------------------------------------
# CREATE
# ---------------------------------------------------------------------------
@router.post(
    "/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
    description="Accepts item data and returns the created item with a generated UUID.",
)
async def create_item(
    payload: ItemCreate,
    service: ItemService = Depends(get_item_service),
) -> ItemResponse:
    """Delegate item creation to the service layer."""

    return await service.create_item(payload)


# ---------------------------------------------------------------------------
# READ (list)
# ---------------------------------------------------------------------------
@router.get(
    "/",
    response_model=ItemListResponse,
    summary="List all items",
    description="Returns every item currently stored in the system.",
)
async def list_items(
    service: ItemService = Depends(get_item_service),
) -> ItemListResponse:
    """Delegate item listing to the service layer."""

    return await service.list_items()


# ---------------------------------------------------------------------------
# READ (single)
# ---------------------------------------------------------------------------
@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Get a single item",
    description="Fetch one item by its UUID. Returns 404 if not found.",
)
async def get_item(
    item_id: UUID,
    service: ItemService = Depends(get_item_service),
) -> ItemResponse:
    """Delegate item retrieval to the service layer."""

    return await service.get_item(item_id)


# ---------------------------------------------------------------------------
# UPDATE
# ---------------------------------------------------------------------------
@router.patch(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Update an item",
    description="Partially update an item. Only provided fields are changed.",
)
async def update_item(
    item_id: UUID,
    payload: ItemUpdate,
    service: ItemService = Depends(get_item_service),
) -> ItemResponse:
    """Delegate item update to the service layer."""

    return await service.update_item(item_id, payload)


# ---------------------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------------------
@router.delete(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Delete an item",
    description="Remove an item by UUID. Returns the deleted item's last state.",
)
async def delete_item(
    item_id: UUID,
    service: ItemService = Depends(get_item_service),
) -> ItemResponse:
    """Delegate item deletion to the service layer."""

    return await service.delete_item(item_id)
