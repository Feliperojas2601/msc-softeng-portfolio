from unittest.mock import AsyncMock

import pytest

from domain.use_cases.count_posts_use_case import CountPostsUseCase


@pytest.fixture
def use_case(mock_post_repository):
    """Fixture providing a CountPostsUseCase wired to a mocked repository."""
    return CountPostsUseCase(mock_post_repository)


async def test_count_return_repository(use_case, mock_post_repository):
    """The use case simply forwards the repository's count."""
    mock_post_repository.count = AsyncMock(return_value=5)

    assert await use_case.execute() == 5
    mock_post_repository.count.assert_called_once()
