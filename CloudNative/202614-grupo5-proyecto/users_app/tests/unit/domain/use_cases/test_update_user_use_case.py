import pytest

from domain.models.user import UserStatus
from domain.use_cases.update_user_use_case import UpdateUserUseCase
from errors import UserNotFoundError


@pytest.fixture
def use_case(mock_user_repository):
    """Fixture providing an UpdateUserUseCase wired to a mocked repository."""
    return UpdateUserUseCase(mock_user_repository)


async def test_execute_raises_when_user_does_not_exist(use_case, mock_user_repository):
    """Updating a missing user raises UserNotFoundError."""
    mock_user_repository.get_by_id.return_value = None

    with pytest.raises(UserNotFoundError):
        await use_case.execute(user_id="missing-id", full_name="New Name")

    mock_user_repository.update.assert_not_called()


async def test_execute_only_overwrites_provided_fields(
    use_case, mock_user_repository, existing_user
):
    """Fields left as None in the request must remain unchanged."""
    mock_user_repository.get_by_id.return_value = existing_user
    mock_user_repository.update.side_effect = lambda user: user

    updated_user = await use_case.execute(
        user_id=existing_user.id, full_name="Jane Doe"
    )

    assert updated_user.full_name == "Jane Doe"
    assert updated_user.dni == existing_user.dni
    assert updated_user.phone_number == existing_user.phone_number
    assert updated_user.status == existing_user.status
    assert updated_user.updated_at >= existing_user.created_at
    mock_user_repository.update.assert_called_once()


async def test_execute_updates_status(use_case, mock_user_repository, existing_user):
    """The status field can be changed to any of the valid values."""
    mock_user_repository.get_by_id.return_value = existing_user
    mock_user_repository.update.side_effect = lambda user: user

    updated_user = await use_case.execute(
        user_id=existing_user.id, status=UserStatus.VERIFICADO
    )

    assert updated_user.status == UserStatus.VERIFICADO


async def test_execute_updates_dni(use_case, mock_user_repository, existing_user):
    """The dni field is overwritten when provided."""
    mock_user_repository.get_by_id.return_value = existing_user
    mock_user_repository.update.side_effect = lambda user: user

    updated_user = await use_case.execute(user_id=existing_user.id, dni="999999999")

    assert updated_user.dni == "999999999"


async def test_execute_updates_phone_number(
    use_case, mock_user_repository, existing_user
):
    """The phone_number field is overwritten when provided."""
    mock_user_repository.get_by_id.return_value = existing_user
    mock_user_repository.update.side_effect = lambda user: user

    updated_user = await use_case.execute(
        user_id=existing_user.id, phone_number="3009999999"
    )

    assert updated_user.phone_number == "3009999999"
