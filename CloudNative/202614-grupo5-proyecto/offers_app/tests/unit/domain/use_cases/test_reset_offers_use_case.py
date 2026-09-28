from unittest.mock import AsyncMock

import pytest

from domain.use_cases.reset_offers_use_case import ResetOffersUseCase


@pytest.fixture
def use_case(mock_offer_repository):
    """Fixture providing a ResetOffersUseCase wired to a mocked repository."""
    return ResetOffersUseCase(mock_offer_repository)


async def test_execute_deletes_all_offers(use_case, mock_offer_repository):
    """The use case delegates the wipe to the repository."""
    mock_offer_repository.reset = AsyncMock(return_value=None)
    await use_case.execute()
    mock_offer_repository.reset.assert_awaited_once()
