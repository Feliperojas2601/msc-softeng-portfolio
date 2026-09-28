from unittest.mock import AsyncMock

import pytest

from domain.use_cases.create_offer_use_case import CreateOfferUseCase
from entrypoints.api.schemas.create_offer import CreateOffer
from errors import InvalidOfferError


@pytest.fixture
def use_case(mock_offer_repository):
    """Fixture providing a CreateOfferUseCase wired to a mocked repository."""
    return CreateOfferUseCase(mock_offer_repository)


async def test_execute_raises_when_size_is_invalid(
    use_case, mock_offer_repository, valid_offer_data
):
    """Creation fails with InvalidOfferError when size is not LARGE, MEDIUM or SMALL."""
    valid_offer_data["size"] = "XLARGE"
    create_offer_schema = CreateOffer(**valid_offer_data)

    with pytest.raises(InvalidOfferError):
        await use_case.execute(create_offer_schema)

    mock_offer_repository.create.assert_not_called()


async def test_execute_raises_when_offer_is_negative(
    use_case, mock_offer_repository, valid_offer_data
):
    """Creation fails with InvalidOfferError when the offer value is negative."""
    valid_offer_data["offer"] = -1
    create_offer_schema = CreateOffer(**valid_offer_data)

    with pytest.raises(InvalidOfferError):
        await use_case.execute(create_offer_schema)

    mock_offer_repository.create.assert_not_called()


async def test_execute_creates_an_offer_successfully(
    use_case, mock_offer_repository, valid_offer_data
):
    """A new offer is created with valid attributes and saved via the repository."""
    mock_offer_repository.create = AsyncMock(side_effect=lambda offer: offer)
    create_offer_schema = CreateOffer(**valid_offer_data)

    created_offer = await use_case.execute(create_offer_schema)

    assert created_offer.postId == str(valid_offer_data["postId"])
    assert created_offer.userId == str(valid_offer_data["userId"])
    assert created_offer.description == valid_offer_data["description"]
    assert created_offer.size == valid_offer_data["size"]
    assert created_offer.fragile == valid_offer_data["fragile"]
    assert created_offer.offer == valid_offer_data["offer"]
    assert created_offer.id is not None
    assert created_offer.createdAt is not None

    mock_offer_repository.create.assert_called_once()
