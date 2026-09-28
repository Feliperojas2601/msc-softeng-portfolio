import json

import httpx
import pytest
import respx

from adapters.http.offers_adapter import HttpOffersAdapter
from domain.models.offer import OfferSize
from errors import DownstreamUnavailableError

BASE = "http://offers.test"


@pytest.fixture
def adapter() -> HttpOffersAdapter:
    """An offers adapter with one retry configured."""
    return HttpOffersAdapter(BASE, timeout=1.0, max_retries=1)


def _create(adapter):
    return adapter.create_offer(
        post_id="post-1",
        user_id="user-1",
        description="Caja",
        size=OfferSize.MEDIUM,
        fragile=True,
        offer=55.0,
    )


@respx.mock
async def test_create_offer_projects_response(adapter):
    """A 201 response is projected into a CreatedOffer."""
    route = respx.post(f"{BASE}/offers").mock(
        return_value=httpx.Response(
            201,
            json={
                "id": "offer-1",
                "userId": "user-1",
                "createdAt": "2026-06-01T12:00:01+00:00",
            },
        )
    )

    offer = await _create(adapter)

    assert offer.id == "offer-1"
    sent = json.loads(route.calls.last.request.content)
    assert sent == {
        "postId": "post-1",
        "userId": "user-1",
        "description": "Caja",
        "size": "MEDIUM",
        "fragile": True,
        "offer": 55.0,
    }


@respx.mock
async def test_create_offer_maps_failure_to_downstream_unavailable(adapter):
    """Any non-201 response becomes DownstreamUnavailableError."""
    respx.post(f"{BASE}/offers").mock(return_value=httpx.Response(500))

    with pytest.raises(DownstreamUnavailableError):
        await _create(adapter)


@respx.mock
async def test_create_offer_is_not_retried(adapter):
    """POST is never retried, even on a transport error."""
    route = respx.post(f"{BASE}/offers")
    route.side_effect = [
        httpx.ConnectError("boom"),
        httpx.Response(
            201, json={"id": "x", "userId": "u", "createdAt": "2026-06-01T00:00:00Z"}
        ),
    ]

    with pytest.raises(DownstreamUnavailableError):
        await _create(adapter)
    assert route.call_count == 1


@respx.mock
async def test_get_offers_by_post_projects_full_offers(adapter):
    """A 200 response is projected into a list of full Offer objects (used by RF-005)."""
    route = respx.get(f"{BASE}/offers").mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "id": "offer-1",
                    "postId": "post-1",
                    "userId": "user-2",
                    "description": "Caja con libros",
                    "size": "SMALL",
                    "fragile": False,
                    "offer": 40.0,
                    "createdAt": "2026-06-01T12:00:00Z",
                }
            ],
        )
    )

    offers = await adapter.get_offers_by_post("post-1")

    assert route.calls.last.request.url.query.decode() == "post=post-1"
    assert len(offers) == 1
    assert offers[0].id == "offer-1"
    assert offers[0].description == "Caja con libros"
    assert offers[0].size == OfferSize.SMALL


@respx.mock
async def test_get_offers_by_post_maps_failure_to_downstream_unavailable(adapter):
    """Any non-200 response becomes DownstreamUnavailableError."""
    respx.get(f"{BASE}/offers").mock(return_value=httpx.Response(500))

    with pytest.raises(DownstreamUnavailableError):
        await adapter.get_offers_by_post("post-1")


@respx.mock
async def test_delete_offer_accepts_200_and_404(adapter):
    """Compensation treats both 200 and 404 as success."""
    respx.delete(f"{BASE}/offers/gone").mock(return_value=httpx.Response(404))
    respx.delete(f"{BASE}/offers/here").mock(return_value=httpx.Response(200))

    await adapter.delete_offer("gone")
    await adapter.delete_offer("here")


@respx.mock
async def test_delete_offer_maps_5xx_to_downstream_unavailable(adapter):
    """A 500 on delete becomes DownstreamUnavailableError."""
    respx.delete(f"{BASE}/offers/offer-1").mock(return_value=httpx.Response(500))

    with pytest.raises(DownstreamUnavailableError):
        await adapter.delete_offer("offer-1")
