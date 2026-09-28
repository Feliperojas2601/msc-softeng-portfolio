from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from assembly import build_send_notification_use_case
from entrypoints.api.main import app
from errors import NotificationPublishError


@pytest.fixture
def client():
    """TestClient for notifications_app."""
    return TestClient(app)


@pytest.fixture
def use_case():
    """AsyncMock bound as the router's use case dependency."""
    mock = AsyncMock()
    app.dependency_overrides[build_send_notification_use_case] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


IDENTITY_BODY = {
    "type": "IDENTITY_VERIFICATION",
    "userId": "u1",
    "email": "john@example.com",
    "fullName": "John Doe",
    "status": "VERIFICADO",
    "ruv": "r1",
}

CREDIT_CARD_BODY = {
    "type": "CREDIT_CARD_VERIFICATION",
    "userId": "u2",
    "email": "jane@example.com",
    "fullName": "Jane Roe",
    "status": "VERIFICADA",
    "ruv": "r2",
    "lastFourDigits": "4242",
    "franchise": "VISA",
}


def test_notify_identity_verification_returns_200(client, use_case):
    """A well-formed identity verification event returns 200."""
    response = client.post("/notify", json=IDENTITY_BODY)

    assert response.status_code == 200
    use_case.execute.assert_called_once_with(
        type="IDENTITY_VERIFICATION",
        user_id="u1",
        email="john@example.com",
        full_name="John Doe",
        status="VERIFICADO",
        ruv="r1",
        last_four_digits=None,
        franchise=None,
    )


def test_notify_credit_card_verification_returns_200(client, use_case):
    """A well-formed credit card verification event returns 200."""
    response = client.post("/notify", json=CREDIT_CARD_BODY)

    assert response.status_code == 200
    use_case.execute.assert_called_once_with(
        type="CREDIT_CARD_VERIFICATION",
        user_id="u2",
        email="jane@example.com",
        full_name="Jane Roe",
        status="VERIFICADA",
        ruv="r2",
        last_four_digits="4242",
        franchise="VISA",
    )


def test_notify_missing_field_returns_400(client, use_case):
    """A body missing a required field is rejected before reaching the use case."""
    body = dict(IDENTITY_BODY)
    del body["ruv"]

    response = client.post("/notify", json=body)

    assert response.status_code == 400
    use_case.execute.assert_not_called()


def test_notify_invalid_type_returns_400(client, use_case):
    """A type outside the known set is rejected."""
    body = {**IDENTITY_BODY, "type": "SOMETHING_ELSE"}

    response = client.post("/notify", json=body)

    assert response.status_code == 400
    use_case.execute.assert_not_called()


def test_notify_publish_failure_returns_502(client, use_case):
    """A failure to publish the notification returns 502."""
    use_case.execute.side_effect = NotificationPublishError("boom")

    response = client.post("/notify", json=IDENTITY_BODY)

    assert response.status_code == 502


def test_ping_returns_pong(client):
    """GET /ping returns a plain text pong."""
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.text == "pong"
