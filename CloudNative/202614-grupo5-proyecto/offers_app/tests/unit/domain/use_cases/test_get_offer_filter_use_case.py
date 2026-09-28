from unittest.mock import AsyncMock

import pytest

from domain.use_cases.get_offer_filter_use_case import GetOfferFiltersUseCase
from entrypoints.api.schemas.offer_filters import OfferFilters


@pytest.fixture
def use_case(mock_offer_repository):
    """Fixture providing a GetOfferFiltersUseCase wired to a mocked repository."""
    return GetOfferFiltersUseCase(mock_offer_repository)


async def test_get_offer_filters_no_filters_returns_all(
    use_case, mock_offer_repository, existing_offer, existing_offer_2
):
    filters = OfferFilters()
    all_offers = [existing_offer, existing_offer_2]
    mock_offer_repository.get_all = AsyncMock(return_value=all_offers)

    result = await use_case.execute(filters)

    assert result == all_offers
    assert len(result) == 2
    mock_offer_repository.get_all.assert_awaited_once_with(filters)


async def test_get_offer_filters_success(
    use_case, mock_offer_repository, existing_offer, existing_offer_2
):
    filters = OfferFilters(post=existing_offer.postId, owner=existing_offer.userId)
    expected_offers = [existing_offer]
    mock_offer_repository.get_all = AsyncMock(return_value=expected_offers)

    result = await use_case.execute(filters)

    assert result == expected_offers
    assert len(result) == 1
    assert existing_offer_2 not in result
    mock_offer_repository.get_all.assert_awaited_once_with(filters)


async def test_get_offer_filters_empty_result(use_case, mock_offer_repository):
    filters = OfferFilters()
    mock_offer_repository.get_all = AsyncMock(return_value=[])

    result = await use_case.execute(filters)

    assert result == []
    mock_offer_repository.get_all.assert_awaited_once_with(filters)
