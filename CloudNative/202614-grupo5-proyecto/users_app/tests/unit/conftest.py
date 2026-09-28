from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from domain.models.user import User, UserStatus
from domain.ports.identity_verification_port import IdentityVerificationPort
from domain.ports.user_repository_port import UserRepositoryPort


@pytest.fixture
def valid_user_data() -> dict:
    """Fixture providing valid raw data to create a user."""
    return {
        "username": "johndoe",
        "password": "S3cret!",
        "email": "johndoe@example.com",
        "dni": "123456789",
        "full_name": "John Doe",
        "phone_number": "3001234567",
    }


@pytest.fixture
def existing_user() -> User:
    """Fixture providing a fully built domain User, as if fetched from storage."""
    now = datetime(2026, 1, 1, 12, 0, 0)
    return User(
        id="a3f1c2d4-0000-4000-8000-000000000001",
        username="johndoe",
        email="johndoe@example.com",
        phone_number="3001234567",
        dni="123456789",
        full_name="John Doe",
        password="hashed-password",
        salt="deadbeef",
        token=None,
        status=UserStatus.POR_VERIFICAR,
        expire_at=None,
        created_at=now,
        updated_at=now,
    )


@pytest.fixture
def mock_user_repository() -> AsyncMock:
    """Fixture providing a fully mocked UserRepositoryPort."""
    return AsyncMock(spec=UserRepositoryPort)


@pytest.fixture
def mock_identity_verification() -> AsyncMock:
    """Fixture providing a fully mocked IdentityVerificationPort."""
    return AsyncMock(spec=IdentityVerificationPort)
