"""Firestore client for caching ArcGIS Hub dataset discovery and field mappings.

Graceful degradation: if Firestore is unavailable (no GCP project configured,
network error, etc.), all operations return None/no-op and log a warning.
The UniversalProvider works without caching — just slower on first lookup.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from plotlot.config import settings
from plotlot.property.models import CountyCache, FieldMapping

logger = logging.getLogger(__name__)

_client = None
_unavailable = False


def _get_client():
    """Lazy-init Firestore client. Returns None if unavailable."""
    global _client, _unavailable  # noqa: PLW0603

    if _unavailable:
        return None
    if _client is not None:
        return _client

    if not settings.gcp_project_id:
        logger.info("Firestore disabled: GCP_PROJECT_ID not set")
        _unavailable = True
        return None

    try:
        from google.cloud.firestore import AsyncClient

        _client = AsyncClient(
            project=settings.gcp_project_id,
            database=settings.firestore_database,
        )
        logger.info("Firestore client initialized for project: %s", settings.gcp_project_id)
        return _client
    except Exception:
        logger.warning("Firestore unavailable — caching disabled", exc_info=True)
        _unavailable = True
        return None


def _collection_name(name: str) -> str:
    """Prefix collection names for namespacing."""
    return f"plotlot_{name}"


async def get_county_cache(county_key: str) -> CountyCache | None:
    """Retrieve cached county data from Firestore.

    Returns None if not cached, expired, or Firestore unavailable.
    """
    client = _get_client()
    if client is None:
        return None

    try:
        doc_ref = client.collection(_collection_name("county_datasets")).document(county_key)
        doc = await doc_ref.get()
        if not doc.exists:
            return None

        cache = CountyCache.model_validate(doc.to_dict())

        # TTL check
        age_hours = (datetime.now(timezone.utc) - cache.last_verified).total_seconds() / 3600
        if age_hours > cache.ttl_hours:
            logger.info("County cache expired for %s (%.1f hours old)", county_key, age_hours)
            return None

        return cache
    except Exception:
        logger.warning("Firestore read failed for county %s", county_key, exc_info=True)
        return None


async def save_county_cache(cache: CountyCache) -> None:
    """Save county cache to Firestore."""
    client = _get_client()
    if client is None:
        return

    try:
        doc_ref = client.collection(_collection_name("county_datasets")).document(cache.county_key)
        await doc_ref.set(cache.model_dump(mode="json"))
        logger.debug("Saved county cache: %s", cache.county_key)
    except Exception:
        logger.warning("Firestore write failed for county %s", cache.county_key, exc_info=True)


async def get_field_mapping(county_key: str) -> FieldMapping | None:
    """Retrieve cached field mapping from Firestore."""
    client = _get_client()
    if client is None:
        return None

    try:
        doc_ref = client.collection(_collection_name("field_mappings")).document(county_key)
        doc = await doc_ref.get()
        if not doc.exists:
            return None
        return FieldMapping.model_validate(doc.to_dict())
    except Exception:
        logger.warning("Firestore read failed for mapping %s", county_key, exc_info=True)
        return None


async def save_field_mapping(mapping: FieldMapping) -> None:
    """Save field mapping to Firestore."""
    client = _get_client()
    if client is None:
        return

    try:
        doc_ref = client.collection(_collection_name("field_mappings")).document(mapping.county_key)
        await doc_ref.set(mapping.model_dump(mode="json"))
        logger.debug("Saved field mapping: %s", mapping.county_key)
    except Exception:
        logger.warning("Firestore write failed for mapping %s", mapping.county_key, exc_info=True)
