from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from domain.models.offer import Offer
from domain.ports.offer_repository_port import OfferRepositoryPort


@pytest.fixture
def valid_offer_data() -> dict:
    """Fixture providing valid raw data to create an offer."""
    return {
        "postId": "9c858901-8a57-4791-81fe-4c455b099bc9",
        "userId": "b3816c65-4f6a-4a6f-8e8f-2e6a9b6f7a11",
        "description": "Paquete pequeño con libros",
        "size": "SMALL",
        "fragile": False,
        "offer": 25.5,
    }


@pytest.fixture
def existing_offer() -> Offer:
    """Fixture providing a fully built domain Offer, as if fetched from storage."""
    now = datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC)
    return Offer(
        id="a3f1c2d4-0000-4000-8000-000000000001",
        postId="9c858901-8a57-4791-81fe-4c455b099bc9",
        userId="b3816c65-4f6a-4a6f-8e8f-2e6a9b6f7a11",
        description="Paquete pequeño con libros",
        size="SMALL",
        fragile=False,
        offer=25.5,
        createdAt=now,
    )


@pytest.fixture
def existing_offer_2() -> Offer:
    """Fixture for a full second Offer."""
    now = datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC)
    return Offer(
        id="c8f9c2d4-9999-4000-8000-000000000099",
        postId="z9y8x7w6-5555-4000-8000-000000000055",
        userId="d4e5f6a1-3333-4000-8000-000000000003",
        description="Paquete grande y frágil",
        size="LARGE",
        fragile=True,
        offer=120,
        createdAt=now,
    )


@pytest.fixture
def mock_offer_repository() -> AsyncMock:
    """Fixture providing a fully mocked OfferRepositoryPort."""
    return AsyncMock(spec=OfferRepositoryPort)
