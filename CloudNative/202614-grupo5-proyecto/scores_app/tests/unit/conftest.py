from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from domain.models.score import Score
from domain.ports.score_repository_port import ScoreRepositoryPort


@pytest.fixture
def valid_score_data() -> dict:
    """Fixture providing valid raw data to create a score."""
    return {
        "offerId": "9c858901-8a57-4791-81fe-4c455b099bc9",
        "size": "MEDIUM",
        "offer": 100.0,
        "bagCost": 20.0,
    }


@pytest.fixture
def existing_score() -> Score:
    """Fixture providing a fully built domain Score, as if fetched from storage."""
    now = datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC)
    return Score(
        id="a3f1c2d4-0000-4000-8000-000000000001",
        offerId="9c858901-8a57-4791-81fe-4c455b099bc9",
        size="MEDIUM",
        offer=100.0,
        bagCost=20.0,
        utility=90.0,
        createdAt=now,
    )


@pytest.fixture
def mock_score_repository() -> AsyncMock:
    """Fixture providing a fully mocked ScoreRepositoryPort."""
    return AsyncMock(spec=ScoreRepositoryPort)
