from datetime import timedelta

import pytest

from domain.models.user import UserStatus
from domain.services.token_service import utcnow
from domain.use_cases.get_current_user_use_case import GetCurrentUserUseCase
from errors import InvalidTokenError


@pytest.fixture
def use_case(mock_user_repository):
    """Fixture providing a GetCurrentUserUseCase wired to a mocked repository."""
    return GetCurrentUserUseCase(mock_user_repository)


async def test_execute_raises_when_token_does_not_exist(use_case, mock_user_repository):
    """An unknown token raises InvalidTokenError."""
    mock_user_repository.get_by_token.return_value = None

    with pytest.raises(InvalidTokenError):
        await use_case.execute("unknown-token")


async def test_execute_raises_when_token_is_expired(
    use_case, mock_user_repository, existing_user
):
    """An expired token raises InvalidTokenError."""
    existing_user.token = "some-token"
    existing_user.expire_at = utcnow() - timedelta(hours=1)
    mock_user_repository.get_by_token.return_value = existing_user

    with pytest.raises(InvalidTokenError):
        await use_case.execute("some-token")


async def test_execute_returns_user_for_a_valid_token(
    use_case, mock_user_repository, existing_user
):
    """A valid, non-expired token resolves to its owning user."""
    existing_user.token = "some-token"
    existing_user.expire_at = utcnow() + timedelta(hours=1)
    existing_user.status = UserStatus.VERIFICADO
    mock_user_repository.get_by_token.return_value = existing_user

    result = await use_case.execute("some-token")

    assert result is existing_user


@pytest.mark.parametrize("status", [UserStatus.POR_VERIFICAR, UserStatus.NO_VERIFICADO])
async def test_execute_raises_when_user_is_not_verified(
    use_case, mock_user_repository, existing_user, status
):
    """A valid token for a non-verified user still raises InvalidTokenError (RF-007)."""
    existing_user.token = "some-token"
    existing_user.expire_at = utcnow() + timedelta(hours=1)
    existing_user.status = status
    mock_user_repository.get_by_token.return_value = existing_user

    with pytest.raises(InvalidTokenError):
        await use_case.execute("some-token")
