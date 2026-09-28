import pytest

from domain.use_cases.reset_users_use_case import ResetUsersUseCase


@pytest.fixture
def use_case(mock_user_repository):
    """Fixture providing a ResetUsersUseCase wired to a mocked repository."""
    return ResetUsersUseCase(mock_user_repository)


async def test_execute_deletes_all_users(use_case, mock_user_repository):
    """The use case delegates the wipe to the repository."""
    await use_case.execute()

    mock_user_repository.delete_all.assert_called_once()
