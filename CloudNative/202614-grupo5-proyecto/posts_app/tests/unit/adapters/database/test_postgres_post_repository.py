from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.database.post_model import PostModel
from adapters.database.postgres_post_repository import SQLAlchemyPostRepositoryAdapter
from entrypoints.api.schemas.post_filters import PostFilters


@pytest.fixture
def mock_session():
    """Fixture providing a fully mocked SQLAlchemy AsyncSession, respecting its sync/async API."""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def adapter(mock_session):
    """Fixture providing a SQLAlchemyPostRepositoryAdapter bound to a mocked session."""
    return SQLAlchemyPostRepositoryAdapter(mock_session)


@pytest.fixture
def sample_post_model(existing_post):
    """Fixture providing a PostModel instance for existing_post."""
    return PostModel(
        id=existing_post.id,
        route_id=existing_post.routeId,
        user_id=existing_post.userId,
        expire_at=existing_post.expireAt,
        created_at=existing_post.createdAt,
    )


@pytest.fixture
def sample_post_model_2(existing_post_2):
    """Fixture providing a PostModel instance for existing_post_2."""
    return PostModel(
        id=existing_post_2.id,
        route_id=existing_post_2.routeId,
        user_id=existing_post_2.userId,
        expire_at=existing_post_2.expireAt,
        created_at=existing_post_2.createdAt,
    )


async def test_create_post(adapter, mock_session, existing_post):
    """Create function adds the post to the session and commits."""
    created = await adapter.create(existing_post)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    assert created.id == existing_post.id


async def test_get_by_id_found(adapter, mock_session, existing_post, sample_post_model):
    """get_by_id returns a Post entity when a record exists."""
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = sample_post_model
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await adapter.get_by_id(existing_post.id)

    mock_session.execute.assert_awaited_once()
    assert result is not None
    assert result.id == existing_post.id


async def test_get_by_id_not_found(adapter, mock_session):
    """get_by_id returns None when no record matches."""
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await adapter.get_by_id("non-existent-id")

    mock_session.execute.assert_awaited_once()
    assert result is None


async def test_get_all_returns_multiple_posts(
    adapter,
    mock_session,
    existing_post,
    existing_post_2,
    sample_post_model,
    sample_post_model_2,
):
    """get_all returns all mapped Post entities when multiple records match."""
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        sample_post_model,
        sample_post_model_2,
    ]
    mock_session.execute = AsyncMock(return_value=mock_result)

    filters = PostFilters(route=None, owner=None, expire=None)
    results = await adapter.get_all(filters)

    mock_session.execute.assert_awaited_once()
    assert len(results) == 2
    assert results[0].id == existing_post.id
    assert results[1].id == existing_post_2.id


async def test_get_all_with_filters(
    adapter, mock_session, existing_post, sample_post_model
):
    """get_all returns filtered posts when matches are found."""
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [sample_post_model]
    mock_session.execute = AsyncMock(return_value=mock_result)

    filters = PostFilters(
        route=existing_post.routeId, owner=existing_post.userId, expire=False
    )
    results = await adapter.get_all(filters)

    mock_session.execute.assert_awaited_once()
    assert len(results) == 1
    assert results[0].id == existing_post.id


async def test_get_all_expired_filter(adapter, mock_session, sample_post_model_2):
    """get_all applies expire=True filter correctly."""
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [sample_post_model_2]
    mock_session.execute = AsyncMock(return_value=mock_result)

    filters = PostFilters(route=None, owner=None, expire=True)
    results = await adapter.get_all(filters)

    mock_session.execute.assert_awaited_once()
    assert len(results) == 1


async def test_delete_post_success(adapter, mock_session, existing_post_2):
    """delete returns True when a row is deleted."""
    mock_result = MagicMock()
    mock_result.rowcount = 1
    mock_session.execute = AsyncMock(return_value=mock_result)

    deleted = await adapter.delete(existing_post_2.id)

    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    assert deleted is True


async def test_delete_post_not_found(adapter, mock_session):
    """delete returns False when no row matches the given ID."""
    mock_result = MagicMock()
    mock_result.rowcount = 0
    mock_session.execute = AsyncMock(return_value=mock_result)

    deleted = await adapter.delete("non-existent-id")

    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    assert deleted is False


async def test_count(adapter, mock_session):
    """count executes a count query and returns total integer."""
    mock_result = MagicMock()
    mock_result.scalar_one.return_value = 2
    mock_session.execute = AsyncMock(return_value=mock_result)

    total = await adapter.count()

    mock_session.execute.assert_awaited_once()
    assert total == 2


async def test_reset(adapter, mock_session):
    """reset executes a bulk delete on PostModel and commits."""
    mock_session.execute = AsyncMock()

    await adapter.reset()

    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
