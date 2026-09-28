from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from domain.models.caller import Caller
from domain.models.offer import Offer, OfferSize
from domain.models.post import Post
from domain.models.route import RouteDetail
from domain.ports.offers_port import OffersPort
from domain.ports.posts_port import PostsPort
from domain.ports.routes_port import RoutesPort
from domain.ports.score_port import ScorePort
from domain.ports.users_port import UsersPort
from domain.use_cases.get_post_rf005_use_case import GetPostRf005UseCase
from errors import (
    DownstreamUnavailableError,
    InvalidTokenError,
    MissingTokenError,
    PostAccessDeniedError,
    PostNotFoundError,
)


@pytest.fixture
def caller() -> Caller:
    """The authenticated caller, owner of the post under test."""
    return Caller(id="user-1", status="VERIFICADO")


@pytest.fixture
def own_post() -> Post:
    """A post owned by the caller."""
    return Post(
        id="post-1",
        route_id="route-1",
        user_id="user-1",
        expire_at=datetime(2026, 12, 31, 23, 59, 59, tzinfo=UTC),
        created_at=datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC),
    )


@pytest.fixture
def route_detail() -> RouteDetail:
    """The full route backing the post, as returned by routes_app."""
    return RouteDetail(
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
    )


@pytest.fixture
def offer_low() -> Offer:
    """An offer with a lower score than offer_high (assigned via score_port)."""
    return Offer(
        id="offer-1",
        user_id="user-2",
        description="Caja con libros",
        size=OfferSize.SMALL,
        fragile=False,
        offer=40.0,
        created_at=datetime(2026, 6, 1, 12, 0, 0, tzinfo=UTC),
    )


@pytest.fixture
def offer_high() -> Offer:
    """An offer with a higher score than offer_low, listed after it on purpose."""
    return Offer(
        id="offer-2",
        user_id="user-3",
        description="Maleta",
        size=OfferSize.LARGE,
        fragile=True,
        offer=90.0,
        created_at=datetime(2026, 6, 1, 13, 0, 0, tzinfo=UTC),
    )


@pytest.fixture
def users_port(caller) -> AsyncMock:
    """Mocked UsersPort that resolves the fixture caller."""
    port = AsyncMock(spec=UsersPort)
    port.get_me.return_value = caller
    return port


@pytest.fixture
def posts_port(own_post) -> AsyncMock:
    """Mocked PostsPort that returns a post owned by the caller."""
    port = AsyncMock(spec=PostsPort)
    port.get_post.return_value = own_post
    return port


@pytest.fixture
def routes_port(route_detail) -> AsyncMock:
    """Mocked RoutesPort that returns the fixture route detail."""
    port = AsyncMock(spec=RoutesPort)
    port.get_route_detail.return_value = route_detail
    return port


@pytest.fixture
def offers_port(offer_low, offer_high) -> AsyncMock:
    """Mocked OffersPort that returns offer_low before offer_high."""
    port = AsyncMock(spec=OffersPort)
    port.get_offers_by_post.return_value = [offer_low, offer_high]
    return port


@pytest.fixture
def score_port() -> AsyncMock:
    """Mocked ScorePort: offer_low -> 10.0, offer_high -> 95.0 (reversed order on purpose)."""
    port = AsyncMock(spec=ScorePort)
    port.get_score.side_effect = [10.0, 95.0]
    return port


@pytest.fixture
def use_case(users_port, posts_port, routes_port, offers_port, score_port):
    """The RF-005 use case wired with mocked ports."""
    return GetPostRf005UseCase(
        users_port, posts_port, routes_port, offers_port, score_port
    )


async def test_happy_path_returns_offers_sorted_descending_by_score(
    use_case, own_post, route_detail
):
    """The result bundles post + route and sorts offers by score, highest first."""
    result = await use_case.execute("token", "post-1")

    assert result.post == own_post
    assert result.route == route_detail
    assert [item.offer.id for item in result.offers] == ["offer-2", "offer-1"]
    assert [item.score for item in result.offers] == [95.0, 10.0]


async def test_offers_without_score_sort_last(use_case, score_port):
    """An offer whose score could not be obtained is placed at the end with score=None."""
    score_port.get_score.side_effect = None
    score_port.get_score.return_value = None

    result = await use_case.execute("token", "post-1")

    assert [item.score for item in result.offers] == [None, None]
    assert {item.offer.id for item in result.offers} == {"offer-1", "offer-2"}


async def test_missing_token_is_rejected_before_any_downstream_call(
    use_case, users_port
):
    """No token short-circuits with 403 and never touches users_app."""
    with pytest.raises(MissingTokenError):
        await use_case.execute(None, "post-1")
    users_port.get_me.assert_not_awaited()


async def test_invalid_token_propagates(use_case, users_port):
    """An invalid token surfaces as InvalidTokenError."""
    users_port.get_me.side_effect = InvalidTokenError()

    with pytest.raises(InvalidTokenError):
        await use_case.execute("bad", "post-1")


async def test_unknown_post_propagates(use_case, posts_port):
    """A missing post surfaces as PostNotFoundError."""
    posts_port.get_post.side_effect = PostNotFoundError()

    with pytest.raises(PostNotFoundError):
        await use_case.execute("token", "ghost")


async def test_non_owner_is_rejected(use_case, posts_port, own_post, routes_port):
    """A caller who does not own the post is rejected with 403 before calling routes_app."""
    own_post.user_id = "someone-else"
    posts_port.get_post.return_value = own_post

    with pytest.raises(PostAccessDeniedError):
        await use_case.execute("token", "post-1")
    routes_port.get_route_detail.assert_not_awaited()


async def test_routes_failure_propagates_as_503(use_case, routes_port, offers_port):
    """A routes_app failure surfaces as 503 and offers are never fetched."""
    routes_port.get_route_detail.side_effect = DownstreamUnavailableError()

    with pytest.raises(DownstreamUnavailableError):
        await use_case.execute("token", "post-1")
    offers_port.get_offers_by_post.assert_not_awaited()


async def test_offers_failure_propagates_as_503(use_case, offers_port, score_port):
    """An offers_app failure surfaces as 503 and no score lookup is attempted."""
    offers_port.get_offers_by_post.side_effect = DownstreamUnavailableError()

    with pytest.raises(DownstreamUnavailableError):
        await use_case.execute("token", "post-1")
    score_port.get_score.assert_not_awaited()


async def test_empty_offers_list_returns_empty_offers(use_case, offers_port):
    """A post with no offers yet returns an empty offers list, not an error."""
    offers_port.get_offers_by_post.return_value = []

    result = await use_case.execute("token", "post-1")

    assert result.offers == []
