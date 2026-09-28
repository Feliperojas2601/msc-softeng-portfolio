import httpx
import pytest
import respx

from adapters.http.users_adapter import HttpUsersAdapter
from errors import DownstreamUnavailableError, InvalidTokenError

BASE = "http://users.test"
ME_URL = f"{BASE}/users/me"


@pytest.fixture
def adapter() -> HttpUsersAdapter:
    """A users adapter with one retry configured."""
    return HttpUsersAdapter(BASE, timeout=1.0, max_retries=1)


@respx.mock
async def test_get_me_returns_caller(adapter):
    """A 200 response is projected into a Caller."""
    respx.get(ME_URL).mock(
        return_value=httpx.Response(200, json={"id": "u1", "status": "VERIFICADO"})
    )

    caller = await adapter.get_me("token")

    assert caller.id == "u1"
    assert caller.status == "VERIFICADO"


@respx.mock
async def test_get_me_sends_bearer_header(adapter):
    """The token is forwarded as a Bearer Authorization header."""
    route = respx.get(ME_URL).mock(return_value=httpx.Response(200, json={"id": "u1"}))

    await adapter.get_me("secret-token")

    assert route.calls.last.request.headers["Authorization"] == "Bearer secret-token"


@respx.mock
@pytest.mark.parametrize("status_code", [401, 403])
async def test_get_me_maps_auth_errors_to_invalid_token(adapter, status_code):
    """401/403 from users_app become InvalidTokenError."""
    respx.get(ME_URL).mock(return_value=httpx.Response(status_code))

    with pytest.raises(InvalidTokenError):
        await adapter.get_me("token")


@respx.mock
async def test_get_me_maps_5xx_to_downstream_unavailable(adapter):
    """A 500 from users_app becomes DownstreamUnavailableError."""
    respx.get(ME_URL).mock(return_value=httpx.Response(500))

    with pytest.raises(DownstreamUnavailableError):
        await adapter.get_me("token")


@respx.mock
async def test_get_me_retries_once_on_transport_error(adapter):
    """A transient connection error is retried and can then succeed."""
    route = respx.get(ME_URL)
    route.side_effect = [
        httpx.ConnectError("boom"),
        httpx.Response(200, json={"id": "u1"}),
    ]

    caller = await adapter.get_me("token")

    assert caller.id == "u1"
    assert route.call_count == 2


@respx.mock
async def test_get_me_gives_up_after_retries(adapter):
    """When every attempt fails at transport level, 503 is raised."""
    respx.get(ME_URL).mock(side_effect=httpx.ConnectError("down"))

    with pytest.raises(DownstreamUnavailableError):
        await adapter.get_me("token")
