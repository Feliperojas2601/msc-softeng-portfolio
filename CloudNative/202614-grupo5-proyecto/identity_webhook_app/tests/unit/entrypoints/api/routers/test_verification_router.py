from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from assembly import build_process_verification_callback_use_case
from entrypoints.api.main import app
from errors import DownstreamUnavailableError, InvalidSignatureError, UserNotFoundError


@pytest.fixture
def client():
    """TestClient for the identity_webhook_app."""
    return TestClient(app)


@pytest.fixture
def use_case():
    """AsyncMock bound as the router's use case dependency."""
    mock = AsyncMock()
    app.dependency_overrides[build_process_verification_callback_use_case] = (
        lambda: mock
    )
    yield mock
    app.dependency_overrides.clear()


VALID_BODY = {
    "RUV": "r1",
    "userIdentifier": "u1",
    "createdAt": "2026-01-01T00:00:00",
    "status": "VERIFICADO",
    "score": 80.42,
    "verifyToken": "whatever",
}


def test_verify_callback_returns_200_on_success(client, use_case):
    """A well-formed, trusted callback returns 200."""
    response = client.patch("/verify-callback", json=VALID_BODY)

    assert response.status_code == 200
    use_case.execute.assert_called_once_with(
        ruv="r1",
        user_id="u1",
        status="VERIFICADO",
        score=80.42,
        verify_token="whatever",
    )


def test_verify_callback_missing_field_returns_400(client, use_case):
    """A body missing a required field is rejected before reaching the use case."""
    body = dict(VALID_BODY)
    del body["score"]

    response = client.patch("/verify-callback", json=body)

    assert response.status_code == 400
    use_case.execute.assert_not_called()


def test_verify_callback_invalid_signature_returns_200(client, use_case):
    """An untrusted callback is acknowledged with 200, not acted on further."""
    use_case.execute.side_effect = InvalidSignatureError("bad signature")

    response = client.patch("/verify-callback", json=VALID_BODY)

    assert response.status_code == 200
    assert response.json() == {"msg": "ignored"}


def test_verify_callback_user_not_found_returns_500(client, use_case):
    """A missing user (should not happen in practice) returns 500."""
    use_case.execute.side_effect = UserNotFoundError("u1")

    response = client.patch("/verify-callback", json=VALID_BODY)

    assert response.status_code == 500


def test_verify_callback_downstream_unavailable_returns_502(client, use_case):
    """users_app being unreachable returns 502."""
    use_case.execute.side_effect = DownstreamUnavailableError("boom")

    response = client.patch("/verify-callback", json=VALID_BODY)

    assert response.status_code == 502


def test_ping_returns_pong(client):
    """GET /ping returns a plain text pong."""
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.text == "pong"
