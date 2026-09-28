import json

import httpx
import pytest
import respx

from adapters.http.users_adapter import HttpUsersAdapter
from errors import DownstreamUnavailableError, UserNotFoundError

BASE = "http://users-app.test"


@pytest.fixture
def adapter() -> HttpUsersAdapter:
    """A users adapter with no retries configured."""
    return HttpUsersAdapter(BASE, timeout=1.0, max_retries=0)


@respx.mock
async def test_get_user_returns_the_parsed_body(adapter):
    """A 200 response is returned as a parsed dict."""
    respx.get(f"{BASE}/users/u1").mock(
        return_value=httpx.Response(200, json={"id": "u1", "email": "a@b.com"})
    )

    user = await adapter.get_user("u1")

    assert user == {"id": "u1", "email": "a@b.com"}


@respx.mock
async def test_get_user_raises_user_not_found_on_404(adapter):
    """A 404 response maps to UserNotFoundError."""
    respx.get(f"{BASE}/users/missing").mock(return_value=httpx.Response(404))

    with pytest.raises(UserNotFoundError):
        await adapter.get_user("missing")


@respx.mock
async def test_get_user_raises_downstream_unavailable_on_unexpected_status(adapter):
    """Any other non-200 status maps to DownstreamUnavailableError."""
    respx.get(f"{BASE}/users/u1").mock(return_value=httpx.Response(500))

    with pytest.raises(DownstreamUnavailableError):
        await adapter.get_user("u1")


@respx.mock
async def test_update_status_sends_the_expected_payload(adapter):
    """PATCH is sent with the new status in the request body."""
    route = respx.patch(f"{BASE}/users/u1").mock(return_value=httpx.Response(200))

    await adapter.update_status("u1", "VERIFICADO")

    assert route.calls.last.request.headers["content-type"] == "application/json"
    assert json.loads(route.calls.last.request.content) == {"status": "VERIFICADO"}


@respx.mock
async def test_update_status_raises_user_not_found_on_404(adapter):
    """A 404 response maps to UserNotFoundError."""
    respx.patch(f"{BASE}/users/missing").mock(return_value=httpx.Response(404))

    with pytest.raises(UserNotFoundError):
        await adapter.update_status("missing", "VERIFICADO")


@respx.mock
async def test_update_status_raises_downstream_unavailable_on_unexpected_status(
    adapter,
):
    """Any other non-200 status maps to DownstreamUnavailableError."""
    respx.patch(f"{BASE}/users/u1").mock(return_value=httpx.Response(400))

    with pytest.raises(DownstreamUnavailableError):
        await adapter.update_status("u1", "VERIFICADO")
