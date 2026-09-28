from datetime import UTC, datetime

import pytest

from domain.models.offer import OfferSize
from domain.use_cases.create_offer_rf004_use_case import CreateOfferRf004UseCase
from errors import (
    DownstreamUnavailableError,
    InvalidTokenError,
    MissingTokenError,
    OfferNotAllowedError,
    PostNotFoundError,
)


@pytest.fixture
def use_case(users_port, posts_port, routes_port, offers_port, score_port, fixed_now):
    """The RF-004 use case wired with mocked ports and a fixed clock."""
    return CreateOfferRf004UseCase(
        users_port,
        posts_port,
        routes_port,
        offers_port,
        score_port,
        now_provider=fixed_now,
    )


async def test_happy_path_creates_offer_with_caller_as_owner(
    use_case, users_port, routes_port, offers_port, score_port, command, created_offer
):
    """The offer is created for the caller; bagCost comes from routes, not scores."""
    result = await use_case.execute("token", "post-1", command)

    assert result == created_offer
    users_port.get_me.assert_awaited_once_with("token")
    routes_port.get_route.assert_awaited_once_with("route-1")
    offers_port.create_offer.assert_awaited_once()
    assert offers_port.create_offer.await_args.kwargs["user_id"] == "user-1"
    assert offers_port.create_offer.await_args.kwargs["post_id"] == "post-1"
    score_port.create_score.assert_awaited_once_with(
        offer_id="offer-1", size=OfferSize.SMALL, offer=40.0, bag_cost=20.0
    )


async def test_routes_failure_propagates_before_the_offer_is_created(
    use_case, routes_port, offers_port, command
):
    """A routes_app failure surfaces as 503 and no offer is created (no compensation)."""
    routes_port.get_route.side_effect = DownstreamUnavailableError()

    with pytest.raises(DownstreamUnavailableError):
        await use_case.execute("token", "post-1", command)
    offers_port.create_offer.assert_not_awaited()


async def test_missing_token_is_rejected_before_any_downstream_call(
    use_case, users_port, command
):
    """No token short-circuits with 403 and never touches users_app."""
    with pytest.raises(MissingTokenError):
        await use_case.execute(None, "post-1", command)
    users_port.get_me.assert_not_awaited()


async def test_invalid_token_propagates(use_case, users_port, command):
    """An invalid token surfaces as InvalidTokenError."""
    users_port.get_me.side_effect = InvalidTokenError()

    with pytest.raises(InvalidTokenError):
        await use_case.execute("bad", "post-1", command)


async def test_unknown_post_propagates(use_case, posts_port, command):
    """A missing post surfaces as PostNotFoundError."""
    posts_port.get_post.side_effect = PostNotFoundError()

    with pytest.raises(PostNotFoundError):
        await use_case.execute("token", "ghost", command)


async def test_expired_post_is_rejected(use_case, posts_port, open_post, command):
    """An offer on an expired post is rejected with 412."""
    open_post.expire_at = datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC)
    posts_port.get_post.return_value = open_post

    with pytest.raises(OfferNotAllowedError):
        await use_case.execute("token", "post-1", command)


async def test_owner_cannot_offer_on_own_post(use_case, posts_port, open_post, command):
    """A caller offering on their own post is rejected with 412."""
    open_post.user_id = "user-1"
    posts_port.get_post.return_value = open_post

    with pytest.raises(OfferNotAllowedError):
        await use_case.execute("token", "post-1", command)


async def test_offers_service_failure_propagates_as_503(
    use_case, offers_port, score_port, command
):
    """A failing offers_app call surfaces as 503 and the score step never runs."""
    offers_port.create_offer.side_effect = DownstreamUnavailableError()

    with pytest.raises(DownstreamUnavailableError):
        await use_case.execute("token", "post-1", command)
    score_port.create_score.assert_not_awaited()


async def test_score_failure_compensates_and_raises(
    use_case, offers_port, score_port, command
):
    """When the score step fails, the created offer is deleted and 503 is raised."""
    score_port.create_score.side_effect = DownstreamUnavailableError()

    with pytest.raises(DownstreamUnavailableError):
        await use_case.execute("token", "post-1", command)
    offers_port.delete_offer.assert_awaited_once_with("offer-1")


async def test_compensation_failure_still_raises_503(
    use_case, offers_port, score_port, command
):
    """A failed compensation is swallowed; the caller still sees 503."""
    score_port.create_score.side_effect = DownstreamUnavailableError()
    offers_port.delete_offer.side_effect = DownstreamUnavailableError()

    with pytest.raises(DownstreamUnavailableError):
        await use_case.execute("token", "post-1", command)
    offers_port.delete_offer.assert_awaited_once_with("offer-1")
