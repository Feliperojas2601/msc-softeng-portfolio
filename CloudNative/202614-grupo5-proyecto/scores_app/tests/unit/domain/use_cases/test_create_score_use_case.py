from unittest.mock import AsyncMock

import pytest

from domain.use_cases.create_score_use_case import CreateScoreUseCase
from entrypoints.api.schemas.create_score import CreateScore
from errors import InvalidScoreError


@pytest.fixture
def use_case(mock_score_repository):
    """Fixture providing a CreateScoreUseCase wired to a mocked repository."""
    return CreateScoreUseCase(mock_score_repository)


async def test_execute_raises_when_size_is_invalid(
    use_case, mock_score_repository, valid_score_data
):
    """Creation fails with InvalidScoreError when size is not LARGE, MEDIUM or SMALL."""
    valid_score_data["size"] = "XLARGE"
    create_score_schema = CreateScore(**valid_score_data)

    with pytest.raises(InvalidScoreError):
        await use_case.execute(create_score_schema)

    mock_score_repository.create.assert_not_called()


@pytest.mark.parametrize(
    "size,occupancy",
    [("LARGE", 1.0), ("MEDIUM", 0.5), ("SMALL", 0.25)],
)
async def test_execute_computes_utility_per_size(
    use_case, mock_score_repository, valid_score_data, size, occupancy
):
    """The utility formula applies the occupancy percentage of each size."""
    mock_score_repository.create = AsyncMock(side_effect=lambda score: score)
    valid_score_data["size"] = size
    valid_score_data["offer"] = 100.0
    valid_score_data["bagCost"] = 40.0
    create_score_schema = CreateScore(**valid_score_data)

    score = await use_case.execute(create_score_schema)

    assert score.utility == 100.0 - (occupancy * 40.0)
    mock_score_repository.create.assert_called_once()


async def test_execute_creates_a_score_successfully(
    use_case, mock_score_repository, valid_score_data
):
    """A new score is calculated with valid attributes and saved via the repository."""
    mock_score_repository.create = AsyncMock(side_effect=lambda score: score)
    create_score_schema = CreateScore(**valid_score_data)

    created_score = await use_case.execute(create_score_schema)

    assert created_score.offerId == valid_score_data["offerId"]
    assert created_score.size == valid_score_data["size"]
    assert created_score.offer == valid_score_data["offer"]
    assert created_score.bagCost == valid_score_data["bagCost"]
    assert created_score.id is not None
    assert created_score.createdAt is not None

    mock_score_repository.create.assert_called_once()
