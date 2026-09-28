import json

import httpx
import pytest
import respx

from adapters.http.score_adapter import HttpScoreAdapter
from domain.models.offer import OfferSize
from errors import DownstreamUnavailableError

BASE = "http://scores.test"


@pytest.fixture
def adapter() -> HttpScoreAdapter:
    """A score adapter with one retry configured."""
    return HttpScoreAdapter(BASE, timeout=1.0, max_retries=1)


def _create(adapter):
    return adapter.create_score(
        offer_id="offer-1",
        size=OfferSize.MEDIUM,
        offer=100.0,
        bag_cost=20.0,
    )


@respx.mock
async def test_create_score_sends_expected_payload(adapter):
    """A 201 response is treated as success and the payload matches the formula inputs."""
    route = respx.post(f"{BASE}/scores").mock(return_value=httpx.Response(201))

    await _create(adapter)

    sent = json.loads(route.calls.last.request.content)
    assert sent == {
        "offerId": "offer-1",
        "size": "MEDIUM",
        "offer": 100.0,
        "bagCost": 20.0,
    }


@respx.mock
async def test_create_score_maps_failure_to_downstream_unavailable(adapter):
    """Any non-201 response becomes DownstreamUnavailableError."""
    respx.post(f"{BASE}/scores").mock(return_value=httpx.Response(500))

    with pytest.raises(DownstreamUnavailableError):
        await _create(adapter)


@respx.mock
async def test_create_score_is_not_retried(adapter):
    """POST is never retried, even on a transport error."""
    route = respx.post(f"{BASE}/scores")
    route.side_effect = [httpx.ConnectError("boom"), httpx.Response(201)]

    with pytest.raises(DownstreamUnavailableError):
        await _create(adapter)
    assert route.call_count == 1


@respx.mock
async def test_get_score_returns_utility_on_200(adapter: HttpScoreAdapter):
    """Un response 200 con un campo utility devuelve ese valor."""
    respx.get(f"{BASE}/scores/offer-1").mock(
        return_value=httpx.Response(200, json={"id": "s1", "utility": 32.5})
    )

    score = await adapter.get_score("offer-1")

    assert score == 32.5


@respx.mock
async def test_get_score_returns_none_on_404(adapter: HttpScoreAdapter):
    """Un response 404 se degrada a None en lugar de lanzar una excepción."""
    respx.get(f"{BASE}/scores/offer-1").mock(return_value=httpx.Response(404))

    assert await adapter.get_score("offer-1") is None


@respx.mock
async def test_get_score_returns_none_when_downstream_unavailable(
    adapter: HttpScoreAdapter,
):
    """Un error de transporte se degrada a None en lugar de lanzar una excepción."""
    route = respx.get(f"{BASE}/scores/offer-1")
    route.side_effect = httpx.ConnectError("boom")

    assert await adapter.get_score("offer-1") is None


@respx.mock
async def test_get_score_returns_none_on_malformed_body(adapter: HttpScoreAdapter):
    """Un response 200 sin el campo utility se degrada a None en lugar de lanzar una excepción."""
    respx.get(f"{BASE}/scores/offer-1").mock(
        return_value=httpx.Response(200, json={"id": "s1"})
    )

    assert await adapter.get_score("offer-1") is None
