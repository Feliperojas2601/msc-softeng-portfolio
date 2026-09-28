import pytest

from domain.use_cases.count_users_use_case import CountUsersUseCase


@pytest.fixture
def use_case(mock_user_repository):
    """Fixture providing a CountUsersUseCase wired to a mocked repository."""
    return CountUsersUseCase(mock_user_repository)


async def test_execute_returns_repository_count(use_case, mock_user_repository):
    """The use case simply forwards the repository's count."""
    mock_user_repository.count.return_value = 5

    assert await use_case.execute() == 5
    mock_user_repository.count.assert_called_once()
