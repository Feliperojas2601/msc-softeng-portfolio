from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from domain.models.post import Post
from domain.ports.post_repository_port import PostRepositoryPort


@pytest.fixture
def valid_post_data() -> dict:
    """Fixture providing valid raw data to create a post."""
    return {
        "routeId": "a1b2c3d4-1111-4000-8000-000000000001",
        "userId": "b2c3d4e5-2222-4000-8000-000000000002",
        "expireAt": datetime.now(UTC) + timedelta(days=7),
    }


@pytest.fixture
def existing_post() -> Post:
    """Fixture providing a fully built domain Post, as if fetched from storage."""
    now = datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC)
    expire = datetime(2026, 1, 15, 12, 0, 0, tzinfo=UTC)
    return Post(
        id="a3f1c2d4-0000-4000-8000-000000000001",
        routeId="a1b2c3d4-1111-4000-8000-000000000001",
        userId="b2c3d4e5-2222-4000-8000-000000000002",
        expireAt=expire,
        createdAt=now,
    )


@pytest.fixture
def existing_post_2() -> Post:
    """Fixture for a full second Post."""
    now = datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC)
    expire = datetime(2026, 1, 15, 12, 0, 0, tzinfo=UTC)
    return Post(
        id="c8f9c2d4-9999-4000-8000-000000000099",
        routeId="z9y8x7w6-5555-4000-8000-000000000055",
        userId="d4e5f6a1-3333-4000-8000-000000000003",
        expireAt=expire,
        createdAt=now,
    )


@pytest.fixture
def mock_post_repository() -> AsyncMock:
    """Fixture providing a fully mocked PostRepositoryPort."""
    return AsyncMock(spec=PostRepositoryPort)
