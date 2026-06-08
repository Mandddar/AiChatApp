"""
Dependency injection providers.

FastAPI's Depends() system wires these into route handlers so
services are created once and shared across the request lifecycle.
"""

from services.item_service import ItemService

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
