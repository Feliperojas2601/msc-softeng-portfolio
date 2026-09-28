from unittest.mock import AsyncMock

import pytest

from domain.use_cases.process_verification_callback_use_case import (
    ProcessVerificationCallbackUseCase,
)
from errors import InvalidSignatureError
from signature import build_verify_token

SECRET = "test-secret"


@pytest.fixture
def users() -> AsyncMock:
    """A mocked UsersPort returning a user with contact data."""
    mock = AsyncMock()
    mock.get_user.return_value = {
        "id": "u1",
        "email": "john@example.com",
        "fullName": "John Doe",
    }
    return mock


@pytest.fixture
def notifications() -> AsyncMock:
    """A mocked NotificationsPort."""
    return AsyncMock()


@pytest.fixture
def use_case(users, notifications) -> ProcessVerificationCallbackUseCase:
    """A use case wired to mocked ports and a known secret."""
    return ProcessVerificationCallbackUseCase(users, notifications, SECRET)


async def test_execute_updates_status_and_notifies_on_valid_signature(
    use_case, users, notifications
):
    """A valid callback updates the user's status and notifies the result."""
    score = 80
    token = build_verify_token(SECRET, "r1", score)

    await use_case.execute(
        ruv="r1", user_id="u1", status="VERIFICADO", score=score, verify_token=token
    )

    users.update_status.assert_called_once_with("u1", "VERIFICADO")
    notifications.notify_identity_result.assert_called_once_with(
        user_id="u1",
        email="john@example.com",
        full_name="John Doe",
        status="VERIFICADO",
        ruv="r1",
    )


async def test_execute_raises_on_invalid_signature(use_case, users, notifications):
    """A tampered verifyToken is rejected and no side effects happen."""
    with pytest.raises(InvalidSignatureError):
        await use_case.execute(
            ruv="r1",
            user_id="u1",
            status="VERIFICADO",
            score=80,
            verify_token="tampered",
        )

    users.get_user.assert_not_called()
    users.update_status.assert_not_called()
    notifications.notify_identity_result.assert_not_called()


async def test_execute_forwards_not_verified_status(use_case, users, notifications):
    """A NO_VERIFICADO result is forwarded as-is to users_app and notifications."""
    score = 40
    token = build_verify_token(SECRET, "r1", score)

    await use_case.execute(
        ruv="r1",
        user_id="u1",
        status="NO_VERIFICADO",
        score=score,
        verify_token=token,
    )

    users.update_status.assert_called_once_with("u1", "NO_VERIFICADO")
