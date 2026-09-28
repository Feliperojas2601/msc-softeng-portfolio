import httpx
import pytest
import respx

from adapters.http.client import request
from errors import IdentityVerificationRequestError

URL = "http://svc.test/thing"


@respx.mock
async def test_request_returns_http_responses_untouched():
    """Even a 500 response is handed back, not raised."""
    respx.get(URL).mock(return_value=httpx.Response(500))

    response = await request("GET", URL, timeout=1.0, max_retries=1)

    assert response.status_code == 500


@respx.mock
async def test_request_retries_get_on_transport_error():
    """A GET is retried on transport failure and can then succeed."""
    route = respx.get(URL)
    route.side_effect = [httpx.ConnectError("boom"), httpx.Response(200)]

    response = await request("GET", URL, timeout=1.0, max_retries=1)

    assert response.status_code == 200
    assert route.call_count == 2


@respx.mock
async def test_request_does_not_retry_non_get():
    """A POST is attempted exactly once on transport failure."""
    route = respx.post(URL).mock(side_effect=httpx.ConnectError("boom"))

    with pytest.raises(IdentityVerificationRequestError):
        await request("POST", URL, timeout=1.0, max_retries=3)
    assert route.call_count == 1


@respx.mock
async def test_request_raises_after_exhausting_retries():
    """When every attempt fails at transport level, the domain error is raised."""
    respx.get(URL).mock(side_effect=httpx.ConnectError("down"))

    with pytest.raises(IdentityVerificationRequestError):
        await request("GET", URL, timeout=1.0, max_retries=2)
