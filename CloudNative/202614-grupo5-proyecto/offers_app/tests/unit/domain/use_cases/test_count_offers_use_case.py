from unittest.mock import AsyncMock

import pytest

from domain.use_cases.count_offers_use_case import CountOffersUseCase


@pytest.fixture
def use_case(mock_offer_repository):
    """Fixture providing a CountOffersUseCase wired to a mocked repository."""
    return CountOffersUseCase(mock_offer_repository)


async def test_count_return_repository(use_case, mock_offer_repository):
    """The use case simply forwards the repository's count."""
    mock_offer_repository.count = AsyncMock(return_value=5)

    assert await use_case.execute() == 5
    mock_offer_repository.count.assert_called_once()
