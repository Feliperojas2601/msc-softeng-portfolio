from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from assembly import build_create_offer_rf004_use_case
from entrypoints.api.main import app
from errors import (
    DownstreamUnavailableError,
    InvalidTokenError,
    MissingTokenError,
    OfferNotAllowedError,
    PostNotFoundError,
)

AUTH = {"Authorization": "Bearer token"}


@pytest.fixture
def client():
    """A TestClient for the orchestrator app."""
    return TestClient(app)


@pytest.fixture
def use_case():
    """An AsyncMock use case bound as the router dependency for the test."""
    mock = AsyncMock()
    app.dependency_overrides[build_create_offer_rf004_use_case] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


def test_create_offer_success_returns_201_envelope(
    client, use_case, created_offer, valid_offer_body
):
    """A successful RF-004 call returns the data envelope with a non-empty msg."""
    use_case.execute.return_value = created_offer

    response = client.post(
        "/rf004/posts/post-1/offers", json=valid_offer_body, headers=AUTH
    )

    assert response.status_code == 201
    body = response.json()
    assert body["data"]["id"] == "offer-1"
    assert body["data"]["userId"] == "user-1"
    assert body["data"]["postId"] == "post-1"
    assert datetime.fromisoformat(body["data"]["createdAt"]) == created_offer.created_at
    assert body["msg"]


def test_missing_body_field_returns_400(client, use_case, valid_offer_body):
    """A missing required field is mapped from 422 to 400."""
    valid_offer_body.pop("description")

    response = client.post(
        "/rf004/posts/post-1/offers", json=valid_offer_body, headers=AUTH
    )

    assert response.status_code == 400
    use_case.execute.assert_not_awaited()


def test_invalid_size_returns_400(client, use_case, valid_offer_body):
    """A size outside the LARGE/MEDIUM/SMALL enum is a 400."""
    response = client.post(
        "/rf004/posts/post-1/offers",
        json={**valid_offer_body, "size": "HUGE"},
        headers=AUTH,
    )

    assert response.status_code == 400


@pytest.mark.parametrize(
    ("error", "expected_status"),
    [
        (MissingTokenError(), 403),
        (InvalidTokenError(), 401),
        (PostNotFoundError(), 404),
        (OfferNotAllowedError(), 412),
        (DownstreamUnavailableError(), 503),
    ],
)
def test_domain_errors_map_to_status_codes(
    client, use_case, valid_offer_body, error, expected_status
):
    """Every orchestrator error is mapped to its HTTP status with a msg body."""
    use_case.execute.side_effect = error

    response = client.post(
        "/rf004/posts/post-1/offers", json=valid_offer_body, headers=AUTH
    )

    assert response.status_code == expected_status
    assert "msg" in response.json()


def test_503_body_carries_the_spec_message(client, use_case, valid_offer_body):
    """The 503 payload matches the message required by the API spec."""
    use_case.execute.side_effect = DownstreamUnavailableError()

    response = client.post(
        "/rf004/posts/post-1/offers", json=valid_offer_body, headers=AUTH
    )

    assert response.json()["msg"] == "El servicio está temporalmente fuera de servicio."


def test_token_is_forwarded_to_the_use_case(client, use_case, valid_offer_body):
    """The bearer token from the request reaches the use case."""
    use_case.execute.side_effect = MissingTokenError()

    client.post(
        "/rf004/posts/post-1/offers",
        json=valid_offer_body,
        headers={"Authorization": "Bearer abc123"},
    )

    assert use_case.execute.await_args.kwargs["token"] == "abc123"


def test_no_auth_header_passes_none_token(client, use_case, valid_offer_body):
    """Without an Authorization header the use case receives token=None."""
    use_case.execute.side_effect = MissingTokenError()

    client.post("/rf004/posts/post-1/offers", json=valid_offer_body)

    assert use_case.execute.await_args.kwargs["token"] is None
