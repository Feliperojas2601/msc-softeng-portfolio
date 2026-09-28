from unittest.mock import AsyncMock

import pytest

from domain.use_cases.delete_offer_use_case import DeleteOfferUseCase
from errors import OfferNotFoundError


@pytest.fixture
def use_case(mock_offer_repository):
    """Fixture providing a DeleteOfferUseCase wired to a mocked repository."""
    return DeleteOfferUseCase(mock_offer_repository)


async def test_delete_offer_invalid_id(use_case, mock_offer_repository):
    invalid_id = "non-existent-id"
    mock_offer_repository.delete = AsyncMock(return_value=False)

    with pytest.raises(OfferNotFoundError):
        await use_case.execute(invalid_id)

    mock_offer_repository.delete.assert_awaited_once_with(invalid_id)


async def test_delete_offer_success(use_case, mock_offer_repository, existing_offer):
    mock_offer_repository.delete = AsyncMock(return_value=True)
    result = await use_case.execute(existing_offer.id)
    assert result is True
    mock_offer_repository.delete.assert_awaited_once_with(existing_offer.id)
