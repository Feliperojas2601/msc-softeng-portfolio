from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.database.offer_model import OfferModel
from adapters.database.postgres_offer_repository import SQLAlchemyOfferRepositoryAdapter
from entrypoints.api.schemas.offer_filters import OfferFilters


@pytest.fixture
def mock_session():
    """Fixture providing a fully mocked SQLAlchemy AsyncSession, respecting its sync/async API."""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def adapter(mock_session):
    """Fixture providing a SQLAlchemyOfferRepositoryAdapter bound to a mocked session."""
    return SQLAlchemyOfferRepositoryAdapter(mock_session)


@pytest.fixture
def sample_offer_model(existing_offer):
    """Fixture providing an OfferModel instance for existing_offer."""
    return OfferModel(
        id=existing_offer.id,
        post_id=existing_offer.postId,
        user_id=existing_offer.userId,
        description=existing_offer.description,
        size=existing_offer.size,
        fragile=existing_offer.fragile,
        offer=existing_offer.offer,
        created_at=existing_offer.createdAt,
    )


@pytest.fixture
def sample_offer_model_2(existing_offer_2):
    """Fixture providing an OfferModel instance for existing_offer_2."""
    return OfferModel(
        id=existing_offer_2.id,
        post_id=existing_offer_2.postId,
        user_id=existing_offer_2.userId,
        description=existing_offer_2.description,
        size=existing_offer_2.size,
        fragile=existing_offer_2.fragile,
        offer=existing_offer_2.offer,
        created_at=existing_offer_2.createdAt,
    )


async def test_create_offer(adapter, mock_session, existing_offer):
    """Create function adds the offer to the session and commits."""
    created = await adapter.create(existing_offer)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    assert created.id == existing_offer.id


async def test_get_by_id_found(
    adapter, mock_session, existing_offer, sample_offer_model
):
    """get_by_id returns an Offer entity when a record exists."""
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = sample_offer_model
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await adapter.get_by_id(existing_offer.id)

    mock_session.execute.assert_awaited_once()
    assert result is not None
    assert result.id == existing_offer.id


async def test_get_by_id_not_found(adapter, mock_session):
    """get_by_id returns None when no record matches."""
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await adapter.get_by_id("non-existent-id")

    mock_session.execute.assert_awaited_once()
    assert result is None


async def test_get_all_returns_multiple_offers(
    adapter,
    mock_session,
    existing_offer,
    existing_offer_2,
    sample_offer_model,
    sample_offer_model_2,
):
    """get_all returns all mapped Offer entities when multiple records match."""
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        sample_offer_model,
        sample_offer_model_2,
    ]
    mock_session.execute = AsyncMock(return_value=mock_result)

    filters = OfferFilters(post=None, owner=None)
    results = await adapter.get_all(filters)

    mock_session.execute.assert_awaited_once()
    assert len(results) == 2
    assert results[0].id == existing_offer.id
    assert results[1].id == existing_offer_2.id


async def test_get_all_with_filters(
    adapter, mock_session, existing_offer, sample_offer_model
):
    """get_all returns filtered offers when matches are found."""
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [sample_offer_model]
    mock_session.execute = AsyncMock(return_value=mock_result)

    filters = OfferFilters(post=existing_offer.postId, owner=existing_offer.userId)
    results = await adapter.get_all(filters)

    mock_session.execute.assert_awaited_once()
    assert len(results) == 1
    assert results[0].id == existing_offer.id


async def test_delete_offer_success(adapter, mock_session, existing_offer_2):
    """delete returns True when a row is deleted."""
    mock_result = MagicMock()
    mock_result.rowcount = 1
    mock_session.execute = AsyncMock(return_value=mock_result)

    deleted = await adapter.delete(existing_offer_2.id)

    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    assert deleted is True


async def test_delete_offer_not_found(adapter, mock_session):
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
    """reset executes a bulk delete on OfferModel and commits."""
    mock_session.execute = AsyncMock()

    await adapter.reset()

    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
