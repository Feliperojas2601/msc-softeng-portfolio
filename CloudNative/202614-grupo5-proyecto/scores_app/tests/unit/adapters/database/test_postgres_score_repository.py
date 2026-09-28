from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.database.postgres_score_repository import SQLAlchemyScoreRepositoryAdapter
from adapters.database.score_model import ScoreModel


@pytest.fixture
def mock_session():
    """Fixture providing a fully mocked SQLAlchemy AsyncSession, respecting its sync/async API."""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def adapter(mock_session):
    """Fixture providing a SQLAlchemyScoreRepositoryAdapter bound to a mocked session."""
    return SQLAlchemyScoreRepositoryAdapter(mock_session)


@pytest.fixture
def sample_score_model(existing_score):
    """Fixture providing a ScoreModel instance for existing_score."""
    return ScoreModel(
        id=existing_score.id,
        offer_id=existing_score.offerId,
        size=existing_score.size,
        offer=existing_score.offer,
        bag_cost=existing_score.bagCost,
        utility=existing_score.utility,
        created_at=existing_score.createdAt,
    )


async def test_create_score(adapter, mock_session, existing_score):
    """Create adds the score to the session and commits."""
    created = await adapter.create(existing_score)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    assert created.id == existing_score.id


async def test_get_by_offer_id_found(
    adapter, mock_session, existing_score, sample_score_model
):
    """get_by_offer_id returns a Score entity when a record exists."""
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = sample_score_model
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await adapter.get_by_offer_id(existing_score.offerId)

    mock_session.execute.assert_awaited_once()
    assert result is not None
    assert result.offerId == existing_score.offerId


async def test_get_by_offer_id_not_found(adapter, mock_session):
    """get_by_offer_id returns None when no score has been calculated yet."""
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await adapter.get_by_offer_id("offer-without-score")

    mock_session.execute.assert_awaited_once()
    assert result is None
