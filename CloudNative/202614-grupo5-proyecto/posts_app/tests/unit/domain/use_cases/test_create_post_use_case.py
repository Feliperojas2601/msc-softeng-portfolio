from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from domain.use_cases.create_post_use_case import CreatePostUseCase
from entrypoints.api.schemas.create_post import CreatePost
from errors import ExpirationDateNoValid


@pytest.fixture
def use_case(mock_post_repository):
    """Fixture providing a CountPostsUseCase wired to a mocked repository."""
    return CreatePostUseCase(mock_post_repository)


async def test_execute_raises_when_expiration_date_is_in_the_past(
    use_case, mock_post_repository, valid_post_data
):
    """Creation fails with ExpirationDateNoValid when expireAt is in the past."""
    valid_post_data["expireAt"] = datetime.now(UTC) - timedelta(days=1)
    create_post_schema = CreatePost(**valid_post_data)

    with pytest.raises(ExpirationDateNoValid):
        await use_case.execute(create_post_schema)

    mock_post_repository.create.assert_not_called()


async def test_execute_raises_when_expiration_date_is_now(
    use_case, mock_post_repository, valid_post_data
):
    """Creation fails with ExpirationDateNoValid when expireAt is less than or equal to current time."""
    valid_post_data["expireAt"] = datetime.now(UTC)
    create_post_schema = CreatePost(**valid_post_data)

    with pytest.raises(ExpirationDateNoValid):
        await use_case.execute(create_post_schema)

    mock_post_repository.create.assert_not_called()


async def test_execute_creates_a_post_successfully(
    use_case, mock_post_repository, valid_post_data
):
    """A new post is created with valid attributes and saved via the repository."""
    mock_post_repository.create = AsyncMock(side_effect=lambda post: post)
    create_post_schema = CreatePost(**valid_post_data)

    created_post = await use_case.execute(create_post_schema)

    assert created_post.routeId == str(valid_post_data["routeId"])
    assert created_post.userId == str(valid_post_data["userId"])
    assert created_post.expireAt == valid_post_data["expireAt"]
    assert created_post.id is not None
    assert created_post.createdAt is not None

    mock_post_repository.create.assert_called_once()
