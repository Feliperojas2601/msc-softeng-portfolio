import pytest

from domain.use_cases.get_user_by_id_use_case import GetUserByIdUseCase
from errors import UserNotFoundError


@pytest.fixture
def use_case(mock_user_repository):
    """Fixture providing a GetUserByIdUseCase wired to a mocked repository."""
    return GetUserByIdUseCase(mock_user_repository)


async def test_execute_returns_user_by_id(
    use_case, mock_user_repository, existing_user
):
    """The use case returns the user found by id."""
    mock_user_repository.get_by_id.return_value = existing_user

    result = await use_case.execute(existing_user.id)

    assert result is existing_user
    mock_user_repository.get_by_id.assert_called_once_with(existing_user.id)


async def test_execute_raises_when_user_does_not_exist(use_case, mock_user_repository):
    """The use case raises UserNotFoundError when no user matches the id."""
    mock_user_repository.get_by_id.return_value = None

    with pytest.raises(UserNotFoundError):
        await use_case.execute("unknown-id")
