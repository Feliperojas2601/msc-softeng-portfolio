from unittest.mock import AsyncMock

import pytest

from domain.use_cases.get_post_use_case import GetPostUseCase
from errors import PostNotFoundError


@pytest.fixture
def use_case(mock_post_repository):
    """Fixture providing a GetPostUseCase wired to a mocked repository."""
    return GetPostUseCase(mock_post_repository)


async def test_get_post_invalid_id(use_case, mock_post_repository):
    invalid_id = "non-existing-id"
    mock_post_repository.get_by_id = AsyncMock(return_value=None)

    with pytest.raises(PostNotFoundError):
        await use_case.execute(invalid_id)

    mock_post_repository.get_by_id.assert_awaited_once_with(invalid_id)


async def test_get_post_success(use_case, mock_post_repository, existing_post):
    mock_post_repository.get_by_id = AsyncMock(return_value=existing_post)
    result = await use_case.execute(existing_post.id)
    assert result == existing_post
    mock_post_repository.get_by_id.assert_awaited_once_with(existing_post.id)
