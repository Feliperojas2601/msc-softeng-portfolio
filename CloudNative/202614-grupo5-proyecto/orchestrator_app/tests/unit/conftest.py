from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from domain.models.caller import Caller
from domain.models.offer import CreatedOffer, CreateOfferCommand, OfferSize
from domain.models.post import Post
from domain.models.route import Route
from domain.ports.offers_port import OffersPort
from domain.ports.posts_port import PostsPort
from domain.ports.routes_port import RoutesPort
from domain.ports.score_port import ScorePort
from domain.ports.users_port import UsersPort

FIXED_NOW = datetime(2026, 6, 1, 12, 0, 0, tzinfo=UTC)


@pytest.fixture
def fixed_now():
    """A deterministic 'now' provider for the RF-004 use case."""
    return lambda: FIXED_NOW


@pytest.fixture
def caller() -> Caller:
    """The authenticated caller resolved from the token."""
    return Caller(id="user-1", status="VERIFICADO")


@pytest.fixture
def open_post() -> Post:
    """A post owned by someone else that is still open for offers."""
    return Post(
        id="post-1",
        route_id="route-1",
        user_id="user-2",
        expire_at=datetime(2026, 12, 31, 23, 59, 59, tzinfo=UTC),
        created_at=datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC),
    )


@pytest.fixture
def route() -> Route:
    """The route backing the post, as returned by routes_app."""
    return Route(id="route-1", bag_cost=20.0)


@pytest.fixture
def created_offer() -> CreatedOffer:
    """The offer as returned by offers_app."""
    return CreatedOffer(
        id="offer-1",
        user_id="user-1",
        created_at=datetime(2026, 6, 1, 12, 0, 1, tzinfo=UTC),
    )


@pytest.fixture
def command() -> CreateOfferCommand:
    """A valid RF-004 offer command."""
    return CreateOfferCommand(
        description="Caja con libros",
        size=OfferSize.SMALL,
        fragile=False,
        offer=40.0,
    )


@pytest.fixture
def users_port(caller) -> AsyncMock:
    """Mocked ``UsersPort`` that resolves the fixture caller."""
    port = AsyncMock(spec=UsersPort)
    port.get_me.return_value = caller
    return port


@pytest.fixture
def posts_port(open_post) -> AsyncMock:
    """Mocked ``PostsPort`` that returns the open post."""
    port = AsyncMock(spec=PostsPort)
    port.get_post.return_value = open_post
    return port


@pytest.fixture
def routes_port(route) -> AsyncMock:
    """Mocked ``RoutesPort`` that returns the fixture route."""
    port = AsyncMock(spec=RoutesPort)
    port.get_route.return_value = route
    return port


@pytest.fixture
def offers_port(created_offer) -> AsyncMock:
    """Mocked ``OffersPort`` that creates the fixture offer."""
    port = AsyncMock(spec=OffersPort)
    port.create_offer.return_value = created_offer
    return port


@pytest.fixture
def score_port() -> AsyncMock:
    """Mocked ``ScorePort`` that succeeds silently."""
    return AsyncMock(spec=ScorePort)


@pytest.fixture
def valid_offer_body() -> dict:
    """Valid JSON body for ``POST /rf004/posts/{id}/offers``."""
    return {
        "description": "Caja con libros",
        "size": "SMALL",
        "fragile": False,
        "offer": 40.0,
    }
