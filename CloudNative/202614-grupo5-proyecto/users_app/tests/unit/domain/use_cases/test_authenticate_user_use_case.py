import pytest

from domain.models.user import UserStatus
from domain.services.password_service import generate_salt, hash_password
from domain.use_cases.authenticate_user_use_case import AuthenticateUserUseCase
from errors import InvalidCredentialsError, UserNotVerifiedError


@pytest.fixture
def use_case(mock_user_repository):
    """Fixture providing an AuthenticateUserUseCase wired to a mocked repository."""
    return AuthenticateUserUseCase(mock_user_repository, token_expiration_hours=24)


async def test_execute_raises_when_user_does_not_exist(use_case, mock_user_repository):
    """Authentication fails with InvalidCredentialsError when the username is unknown."""
    mock_user_repository.get_by_username.return_value = None

    with pytest.raises(InvalidCredentialsError):
        await use_case.execute(username="ghost", password="whatever")


async def test_execute_raises_when_password_does_not_match(
    use_case, mock_user_repository, existing_user
):
    """Authentication fails with InvalidCredentialsError when the password is wrong."""
    salt = generate_salt()
    existing_user.salt = salt
    existing_user.password = hash_password("correct-password", salt)
    mock_user_repository.get_by_username.return_value = existing_user

    with pytest.raises(InvalidCredentialsError):
        await use_case.execute(
            username=existing_user.username, password="wrong-password"
        )

    mock_user_repository.update.assert_not_called()


async def test_execute_issues_a_new_token_on_success(
    use_case, mock_user_repository, existing_user
):
    """A successful authentication stores a fresh token and expiration on the user."""
    salt = generate_salt()
    existing_user.salt = salt
    existing_user.password = hash_password("correct-password", salt)
    existing_user.token = None
    existing_user.status = UserStatus.VERIFICADO
    mock_user_repository.get_by_username.return_value = existing_user
    mock_user_repository.update.side_effect = lambda user: user

    authenticated_user = await use_case.execute(
        username=existing_user.username, password="correct-password"
    )

    assert authenticated_user.token is not None
    assert authenticated_user.expire_at is not None
    mock_user_repository.update.assert_called_once()


@pytest.mark.parametrize("status", [UserStatus.POR_VERIFICAR, UserStatus.NO_VERIFICADO])
async def test_execute_raises_when_user_is_not_verified(
    use_case, mock_user_repository, existing_user, status
):
    """Authentication fails with UserNotVerifiedError for non-verified users (RF-007)."""
    salt = generate_salt()
    existing_user.salt = salt
    existing_user.password = hash_password("correct-password", salt)
    existing_user.status = status
    mock_user_repository.get_by_username.return_value = existing_user

    with pytest.raises(UserNotVerifiedError):
        await use_case.execute(
            username=existing_user.username, password="correct-password"
        )

    mock_user_repository.update.assert_not_called()
