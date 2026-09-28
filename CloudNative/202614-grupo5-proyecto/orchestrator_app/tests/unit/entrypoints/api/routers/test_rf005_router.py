from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from assembly import build_get_post_rf005_use_case
from domain.models.offer import Offer, OfferSize
from domain.models.post import Post
from domain.models.post_detail import OfferWithScore, PostDetail
from domain.models.route import RouteDetail
from entrypoints.api.main import app
from errors import (
    DownstreamUnavailableError,
    InvalidTokenError,
    MissingTokenError,
    PostAccessDeniedError,
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
    app.dependency_overrides[build_get_post_rf005_use_case] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


@pytest.fixture
def post_detail() -> PostDetail:
    """A full RF-005 result: a post, its route and one scored offer."""
    return PostDetail(
        post=Post(
            id="post-1",
            route_id="route-1",
            user_id="user-1",
            expire_at=datetime(2026, 12, 31, 23, 59, 59, tzinfo=UTC),
            created_at=datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC),
        ),
        route=RouteDetail(
            id="route-1",
            flightId="AV123",
            sourceAirportCode="BOG",
            sourceCountry="Colombia",
            destinyAirportCode="MIA",
            destinyCountry="Estados Unidos",
            bagCost=20.0,
            plannedStartDate=datetime(2026, 6, 10, 8, 0, 0, tzinfo=UTC),
            plannedEndDate=datetime(2026, 6, 10, 12, 0, 0, tzinfo=UTC),
            createdAt=datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC),
        ),
        offers=[
            OfferWithScore(
                offer=Offer(
                    id="offer-1",
                    user_id="user-2",
                    description="Caja con libros",
                    size=OfferSize.SMALL,
                    fragile=False,
                    offer=40.0,
                    created_at=datetime(2026, 6, 1, 12, 0, 0, tzinfo=UTC),
                ),
                score=95.0,
            )
        ],
    )


def test_get_post_success_returns_data_envelope(client, use_case, post_detail):
    """A successful RF-005 call returns the publication, route and offers with score."""
    use_case.execute.return_value = post_detail

    response = client.get("/rf005/posts/post-1", headers=AUTH)

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["id"] == "post-1"
    assert body["data"]["route"]["flightId"] == "AV123"
    assert body["data"]["route"]["origin"]["airportCode"] == "BOG"
    assert body["data"]["plannedStartDate"] is not None
    assert body["data"]["offers"][0]["id"] == "offer-1"
    assert body["data"]["offers"][0]["score"] == 95.0


def test_offer_with_null_score_is_preserved_in_response(client, use_case, post_detail):
    """An offer without a score is serialized with score: null, not dropped."""
    post_detail.offers[0].score = None
    use_case.execute.return_value = post_detail

    response = client.get("/rf005/posts/post-1", headers=AUTH)

    assert response.json()["data"]["offers"][0]["score"] is None


@pytest.mark.parametrize(
    ("error", "expected_status"),
    [
        (MissingTokenError(), 403),
        (InvalidTokenError(), 401),
        (PostNotFoundError(), 404),
        (PostAccessDeniedError(), 403),
        (DownstreamUnavailableError(), 503),
    ],
)
def test_domain_errors_map_to_status_codes(client, use_case, error, expected_status):
    """Every orchestrator error raised by the use case maps to its HTTP status."""
    use_case.execute.side_effect = error

    response = client.get("/rf005/posts/post-1", headers=AUTH)

    assert response.status_code == expected_status
    assert "msg" in response.json()


def test_no_auth_header_passes_none_token(client, use_case):
    """Without an Authorization header the use case receives token=None."""
    use_case.execute.side_effect = MissingTokenError()

    client.get("/rf005/posts/post-1")

    assert use_case.execute.await_args.kwargs["token"] is None


def test_token_is_forwarded_to_the_use_case(client, use_case, post_detail):
    """The bearer token from the request reaches the use case."""
    use_case.execute.return_value = post_detail

    client.get("/rf005/posts/post-1", headers={"Authorization": "Bearer abc123"})

    assert use_case.execute.await_args.kwargs["token"] == "abc123"
