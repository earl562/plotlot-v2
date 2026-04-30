"""Unit-test fixtures for FastAPI endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from plotlot.api.main import app


@pytest.fixture
def transport():
    return ASGITransport(app=app)


@pytest.fixture
async def client(transport):
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
