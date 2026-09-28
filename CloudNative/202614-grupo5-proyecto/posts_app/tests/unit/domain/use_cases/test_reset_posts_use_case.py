from unittest.mock import AsyncMock

import pytest

from domain.use_cases.reset_posts_use_case import ResetPostsUseCase


@pytest.fixture
def use_case(mock_post_repository):
    """Fixture providing a ResetPostsUseCase wired to a mocked repository."""
    return ResetPostsUseCase(mock_post_repository)


async def test_execute_deletes_all_posts(use_case, mock_post_repository):
    """The use case delegates the wipe to the repository."""
    mock_post_repository.reset = AsyncMock(return_value=None)
    await use_case.execute()
    mock_post_repository.reset.assert_awaited_once()
