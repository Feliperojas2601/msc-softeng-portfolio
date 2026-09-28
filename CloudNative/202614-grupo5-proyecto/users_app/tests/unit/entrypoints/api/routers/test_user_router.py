from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from assembly import (
    build_authenticate_user_use_case,
    build_count_users_use_case,
    build_create_user_use_case,
    build_get_current_user_use_case,
    build_get_user_by_id_use_case,
    build_reset_users_use_case,
    build_update_user_use_case,
)
from domain.models.user import UserStatus
from domain.services.password_service import generate_salt, hash_password
from domain.services.token_service import utcnow
from domain.use_cases.authenticate_user_use_case import AuthenticateUserUseCase
from entrypoints.api.main import app
from errors import (
    InvalidCredentialsError,
    InvalidTokenError,
    UserAlreadyExistsError,
    UserNotFoundError,
    UserNotVerifiedError,
)


@pytest.fixture
def client():
    """Fixture providing a TestClient that never runs the app's lifespan (no real DB)."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_overrides():
    """Ensure dependency overrides never leak between tests."""
    yield
    app.dependency_overrides.clear()


def _override(builder, use_case):
    app.dependency_overrides[builder] = lambda: use_case


def test_create_user_returns_201(client, existing_user):
    """POST /users returns 201 with id and createdAt on success."""
    use_case = AsyncMock()
    use_case.execute.return_value = existing_user
    _override(build_create_user_use_case, use_case)

    response = client.post(
        "/users",
        json={
            "username": "johndoe",
            "password": "secret",
            "email": "johndoe@example.com",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == existing_user.id
    assert "createdAt" in body


def test_create_user_missing_fields_returns_400(client):
    """POST /users with missing required fields returns 400, not FastAPI's default 422."""
    response = client.post("/users", json={"username": "johndoe"})

    assert response.status_code == 400


def test_create_user_already_exists_returns_412(client):
    """POST /users returns 412 when the domain use case reports a duplicate."""
    use_case = AsyncMock()
    use_case.execute.side_effect = UserAlreadyExistsError()
    _override(build_create_user_use_case, use_case)

    response = client.post(
        "/users",
        json={
            "username": "johndoe",
            "password": "secret",
            "email": "johndoe@example.com",
        },
    )

    assert response.status_code == 412


def test_update_user_returns_200(client):
    """PATCH /users/{id} returns 200 with a confirmation message."""
    use_case = AsyncMock()
    _override(build_update_user_use_case, use_case)

    response = client.patch("/users/some-id", json={"fullName": "Jane Doe"})

    assert response.status_code == 200
    assert response.json() == {"msg": "el usuario ha sido actualizado"}


def test_update_user_empty_body_returns_400(client):
    """PATCH /users/{id} with no updatable fields returns 400."""
    response = client.patch("/users/some-id", json={})

    assert response.status_code == 400


def test_update_user_not_found_returns_404(client):
    """PATCH /users/{id} returns 404 when the use case reports a missing user."""
    use_case = AsyncMock()
    use_case.execute.side_effect = UserNotFoundError()
    _override(build_update_user_use_case, use_case)

    response = client.patch("/users/missing-id", json={"fullName": "Jane Doe"})

    assert response.status_code == 404


def test_authenticate_user_returns_200(client, existing_user):
    """POST /users/auth returns 200 with id, token and expireAt."""
    existing_user.token = "some-token"
    existing_user.expire_at = utcnow()
    use_case = AsyncMock()
    use_case.execute.return_value = existing_user
    _override(build_authenticate_user_use_case, use_case)

    response = client.post(
        "/users/auth", json={"username": "johndoe", "password": "secret"}
    )

    assert response.status_code == 200
    assert response.json()["token"] == "some-token"


def test_authenticate_user_invalid_credentials_returns_404(client):
    """POST /users/auth returns 404 when credentials do not match."""
    use_case = AsyncMock()
    use_case.execute.side_effect = InvalidCredentialsError()
    _override(build_authenticate_user_use_case, use_case)

    response = client.post(
        "/users/auth", json={"username": "johndoe", "password": "wrong"}
    )

    assert response.status_code == 404


def test_authenticate_user_not_verified_returns_401(client):
    use_case = AsyncMock()
    use_case.execute.side_effect = UserNotVerifiedError()
    _override(build_authenticate_user_use_case, use_case)

    response = client.post(
        "/users/auth", json={"username": "johndoe", "password": "secret"}
    )

    assert response.status_code == 401


@pytest.mark.parametrize("status", [UserStatus.POR_VERIFICAR, UserStatus.NO_VERIFICADO])
def test_unverified_user_never_receives_or_persists_token(
    client, existing_user, mock_user_repository, status
):
    existing_user.status = status
    existing_user.salt = generate_salt()
    existing_user.password = hash_password("secret", existing_user.salt)
    previous_updated_at = existing_user.updated_at
    mock_user_repository.get_by_username.return_value = existing_user
    _override(
        build_authenticate_user_use_case,
        AuthenticateUserUseCase(mock_user_repository, token_expiration_hours=24),
    )

    with patch(
        "domain.use_cases.authenticate_user_use_case.generate_token"
    ) as generate_token:
        response = client.post(
            "/users/auth",
            json={"username": existing_user.username, "password": "secret"},
        )

    assert response.status_code == 401
    assert response.json() == {}
    generate_token.assert_not_called()
    mock_user_repository.update.assert_not_called()
    assert existing_user.token is None
    assert existing_user.expire_at is None
    assert existing_user.updated_at == previous_updated_at


def test_get_me_without_authorization_header_returns_403(client):
    """GET /users/me without an Authorization header returns 403."""
    response = client.get("/users/me")

    assert response.status_code == 403


def test_get_me_with_invalid_token_returns_401(client):
    """GET /users/me with an invalid/expired token returns 401."""
    use_case = AsyncMock()
    use_case.execute.side_effect = InvalidTokenError()
    _override(build_get_current_user_use_case, use_case)

    response = client.get(
        "/users/me", headers={"Authorization": "Bearer invalid-token"}
    )

    assert response.status_code == 401


def test_get_me_with_valid_token_returns_200(client, existing_user):
    """GET /users/me with a valid token returns the user's public profile."""
    use_case = AsyncMock()
    use_case.execute.return_value = existing_user
    _override(build_get_current_user_use_case, use_case)

    response = client.get("/users/me", headers={"Authorization": "Bearer valid-token"})

    assert response.status_code == 200
    assert response.json()["username"] == existing_user.username


def test_count_users_returns_200(client):
    """GET /users/count returns the total number of users."""
    use_case = AsyncMock()
    use_case.execute.return_value = 3
    _override(build_count_users_use_case, use_case)

    response = client.get("/users/count")

    assert response.status_code == 200
    assert response.json() == {"count": 3}


def test_ping_returns_pong(client):
    """GET /users/ping returns a plain text pong."""
    response = client.get("/users/ping")

    assert response.status_code == 200
    assert response.text == "pong"


def test_get_user_by_id_returns_200(client, existing_user):
    """GET /users/{id} returns the user's public profile."""
    use_case = AsyncMock()
    use_case.execute.return_value = existing_user
    _override(build_get_user_by_id_use_case, use_case)

    response = client.get(f"/users/{existing_user.id}")

    assert response.status_code == 200
    assert response.json()["id"] == existing_user.id
    assert response.json()["email"] == existing_user.email
    assert "password" not in response.json()
    assert "token" not in response.json()


def test_get_user_by_id_not_found_returns_404(client):
    """GET /users/{id} returns 404 when no user matches the id."""
    use_case = AsyncMock()
    use_case.execute.side_effect = UserNotFoundError()
    _override(build_get_user_by_id_use_case, use_case)

    response = client.get("/users/missing-id")

    assert response.status_code == 404


def test_reset_users_returns_200(client):
    """POST /users/reset returns a confirmation message."""
    use_case = AsyncMock()
    _override(build_reset_users_use_case, use_case)

    response = client.post("/users/reset")

    assert response.status_code == 200
    assert response.json() == {"msg": "Todos los datos fueron eliminados"}
    use_case.execute.assert_awaited_once()
