from unittest.mock import AsyncMock

import pytest

from domain.use_cases.get_score_use_case import GetScoreUseCase
from errors import ScoreNotFoundError


@pytest.fixture
def use_case(mock_score_repository):
    """Fixture providing a GetScoreUseCase wired to a mocked repository."""
    return GetScoreUseCase(mock_score_repository)


async def test_get_score_missing_raises_not_found(use_case, mock_score_repository):
    """The offer without a calculated score raises ScoreNotFoundError."""
    mock_score_repository.get_by_offer_id = AsyncMock(return_value=None)

    with pytest.raises(ScoreNotFoundError):
        await use_case.execute("offer-without-score")

    mock_score_repository.get_by_offer_id.assert_awaited_once_with(
        "offer-without-score"
    )


async def test_get_score_success(use_case, mock_score_repository, existing_score):
    """An existing score is returned unchanged."""
    mock_score_repository.get_by_offer_id = AsyncMock(return_value=existing_score)

    result = await use_case.execute(existing_score.offerId)

    assert result == existing_score
    mock_score_repository.get_by_offer_id.assert_awaited_once_with(
        existing_score.offerId
    )
