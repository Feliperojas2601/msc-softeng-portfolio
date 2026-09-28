import pytest
from pydantic import ValidationError

from domain.services.token_service import utcnow
from entrypoints.api.schemas.user_schemas import (
    AuthResponse,
    CreateUserRequest,
    CreateUserResponse,
    MeResponse,
    UpdateUserRequest,
)


def test_create_user_request_accepts_camel_case_payload():
    """CreateUserRequest parses the camelCase body defined by the API spec."""
    request = CreateUserRequest.model_validate(
        {
            "username": "johndoe",
            "password": "secret",
            "email": "johndoe@example.com",
            "dni": "123",
            "fullName": "John Doe",
            "phoneNumber": "3000000000",
        }
    )

    assert request.full_name == "John Doe"
    assert request.phone_number == "3000000000"


@pytest.mark.parametrize("username", ["john doe", "john!", "john-doe", ""])
def test_create_user_request_rejects_invalid_usernames(username):
    """Usernames with spaces or special characters are rejected."""
    with pytest.raises(ValidationError):
        CreateUserRequest(
            username=username, password="secret", email="johndoe@example.com"
        )


def test_create_user_request_rejects_invalid_email():
    """An invalid email format is rejected."""
    with pytest.raises(ValidationError):
        CreateUserRequest(username="johndoe", password="secret", email="not-an-email")


def test_create_user_response_serializes_using_camel_case(existing_user):
    """CreateUserResponse exposes createdAt in the JSON output."""
    response = CreateUserResponse.from_user(existing_user)

    assert response.model_dump(by_alias=True) == {
        "id": existing_user.id,
        "createdAt": existing_user.created_at,
    }


def test_update_user_request_rejects_empty_body():
    """UpdateUserRequest requires at least one updatable field."""
    with pytest.raises(ValidationError):
        UpdateUserRequest()


def test_update_user_request_accepts_a_single_field():
    """UpdateUserRequest accepts a body with only one of the allowed fields."""
    request = UpdateUserRequest.model_validate({"fullName": "Jane Doe"})

    assert request.full_name == "Jane Doe"
    assert request.status is None


def test_me_response_from_user(existing_user):
    """MeResponse exposes the public profile fields of a domain User."""
    response = MeResponse.from_user(existing_user)

    dumped = response.model_dump(by_alias=True)
    assert dumped["fullName"] == existing_user.full_name
    assert "password" not in dumped
    assert "salt" not in dumped
    assert "token" not in dumped


def test_auth_response_from_user(existing_user):
    """AuthResponse exposes only id, token and expireAt."""
    existing_user.token = "some-token"
    existing_user.expire_at = utcnow()

    response = AuthResponse.from_user(existing_user)

    assert response.token == "some-token"
    assert response.model_dump(by_alias=True)["expireAt"] == existing_user.expire_at
