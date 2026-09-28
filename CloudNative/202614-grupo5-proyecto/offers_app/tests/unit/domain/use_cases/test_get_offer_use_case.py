from unittest.mock import AsyncMock

import pytest

from domain.use_cases.get_offer_use_case import GetOfferUseCase
from errors import OfferNotFoundError


@pytest.fixture
def use_case(mock_offer_repository):
    """Fixture providing a GetOfferUseCase wired to a mocked repository."""
    return GetOfferUseCase(mock_offer_repository)


async def test_get_offer_invalid_id(use_case, mock_offer_repository):
    invalid_id = "non-existing-id"
    mock_offer_repository.get_by_id = AsyncMock(return_value=None)

    with pytest.raises(OfferNotFoundError):
        await use_case.execute(invalid_id)

    mock_offer_repository.get_by_id.assert_awaited_once_with(invalid_id)


async def test_get_offer_success(use_case, mock_offer_repository, existing_offer):
    mock_offer_repository.get_by_id = AsyncMock(return_value=existing_offer)
    result = await use_case.execute(existing_offer.id)
    assert result == existing_offer
    mock_offer_repository.get_by_id.assert_awaited_once_with(existing_offer.id)
