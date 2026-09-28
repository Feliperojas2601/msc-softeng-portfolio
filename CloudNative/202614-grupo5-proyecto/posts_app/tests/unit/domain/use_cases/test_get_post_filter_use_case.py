from unittest.mock import AsyncMock

import pytest

from domain.use_cases.get_post_filter_use_case import GetPostFiltersUseCase
from entrypoints.api.schemas.post_filters import PostFilters


@pytest.fixture
def use_case(mock_post_repository):
    """Fixture providing a GetPostFiltersUseCase wired to a mocked repository."""
    return GetPostFiltersUseCase(mock_post_repository)


async def test_get_post_filters_no_filters_returns_all(
    use_case, mock_post_repository, existing_post, existing_post_2
):
    filters = PostFilters()
    all_posts = [existing_post, existing_post_2]
    mock_post_repository.get_all = AsyncMock(return_value=all_posts)

    result = await use_case.execute(filters)

    assert result == all_posts
    assert len(result) == 2
    mock_post_repository.get_all.assert_awaited_once_with(filters)


async def test_get_post_filters_success(
    use_case, mock_post_repository, existing_post, existing_post_2
):
    filters = PostFilters(
        route=existing_post.routeId, owner=existing_post.userId, expire=False
    )
    expected_posts = [existing_post]
    mock_post_repository.get_all = AsyncMock(return_value=expected_posts)

    result = await use_case.execute(filters)

    assert result == expected_posts
    assert len(result) == 1
    assert existing_post_2 not in result
    mock_post_repository.get_all.assert_awaited_once_with(filters)


async def test_get_post_filters_empty_result(
    use_case,
    mock_post_repository,
):
    filters = PostFilters()
    mock_post_repository.get_all = AsyncMock(return_value=[])

    result = await use_case.execute(filters)

    assert result == []
    mock_post_repository.get_all.assert_awaited_once_with(filters)
