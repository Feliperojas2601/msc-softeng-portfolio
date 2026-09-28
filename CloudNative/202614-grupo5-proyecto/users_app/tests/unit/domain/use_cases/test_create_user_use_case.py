import pytest

from domain.models.user import UserStatus
from domain.services.password_service import verify_password
from domain.use_cases.create_user_use_case import CreateUserUseCase
from errors import IdentityVerificationRequestError, UserAlreadyExistsError

WEBHOOK_URL = "https://example.com/native/verify-callback"


@pytest.fixture
def use_case(mock_user_repository, mock_identity_verification):
    """Fixture providing a CreateUserUseCase wired to mocked dependencies."""
    return CreateUserUseCase(
        mock_user_repository, mock_identity_verification, WEBHOOK_URL
    )


async def test_execute_raises_when_username_already_exists(
    use_case, mock_user_repository, valid_user_data, existing_user
):
    """Creation fails with UserAlreadyExistsError when the username is taken."""
    mock_user_repository.get_by_username.return_value = existing_user
    mock_user_repository.get_by_email.return_value = None

    with pytest.raises(UserAlreadyExistsError):
        await use_case.execute(**valid_user_data)

    mock_user_repository.create.assert_not_called()


async def test_execute_raises_when_email_already_exists(
    use_case, mock_user_repository, valid_user_data, existing_user
):
    """Creation fails with UserAlreadyExistsError when the email is taken."""
    mock_user_repository.get_by_username.return_value = None
    mock_user_repository.get_by_email.return_value = existing_user

    with pytest.raises(UserAlreadyExistsError):
        await use_case.execute(**valid_user_data)

    mock_user_repository.create.assert_not_called()


async def test_execute_creates_a_user_with_hashed_password_and_default_status(
    use_case, mock_user_repository, mock_identity_verification, valid_user_data
):
    """A new user is created with POR_VERIFICAR status and a hashed password."""
    mock_user_repository.get_by_username.return_value = None
    mock_user_repository.get_by_email.return_value = None
    mock_user_repository.create.side_effect = lambda user: user

    created_user = await use_case.execute(**valid_user_data)

    assert created_user.username == valid_user_data["username"]
    assert created_user.email == valid_user_data["email"]
    assert created_user.status == UserStatus.POR_VERIFICAR
    assert created_user.password != valid_user_data["password"]
    assert verify_password(
        valid_user_data["password"], created_user.salt, created_user.password
    )
    mock_user_repository.create.assert_called_once()
    mock_identity_verification.request_verification.assert_called_once()
    call_kwargs = mock_identity_verification.request_verification.call_args.kwargs
    assert call_kwargs["user_id"] == created_user.id
    assert call_kwargs["webhook_url"] == WEBHOOK_URL
    assert call_kwargs["email"] == created_user.email


async def test_execute_still_creates_the_user_when_verification_request_fails(
    use_case, mock_user_repository, mock_identity_verification, valid_user_data
):
    """A failure to reach the identity provider does not prevent user creation."""
    mock_user_repository.get_by_username.return_value = None
    mock_user_repository.get_by_email.return_value = None
    mock_user_repository.create.side_effect = lambda user: user
    mock_identity_verification.request_verification.side_effect = (
        IdentityVerificationRequestError()
    )

    created_user = await use_case.execute(**valid_user_data)

    assert created_user.status == UserStatus.POR_VERIFICAR
    mock_user_repository.create.assert_called_once()
