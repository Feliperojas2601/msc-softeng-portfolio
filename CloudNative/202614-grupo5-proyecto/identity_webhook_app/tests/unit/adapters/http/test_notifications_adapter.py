import json

import httpx
import pytest
import respx

from adapters.http.notifications_adapter import HttpNotificationsAdapter

BASE = "http://notifications-app.test"


@pytest.fixture
def adapter() -> HttpNotificationsAdapter:
    """A notifications adapter with no retries configured."""
    return HttpNotificationsAdapter(BASE, timeout=1.0, max_retries=0)


@respx.mock
async def test_notify_identity_result_sends_the_expected_payload(adapter):
    """The published payload matches the documented event contract."""
    route = respx.post(f"{BASE}/notify").mock(return_value=httpx.Response(200))

    await adapter.notify_identity_result(
        user_id="u1",
        email="john@example.com",
        full_name="John Doe",
        status="VERIFICADO",
        ruv="r1",
    )

    assert json.loads(route.calls.last.request.content) == {
        "type": "IDENTITY_VERIFICATION",
        "userId": "u1",
        "email": "john@example.com",
        "fullName": "John Doe",
        "status": "VERIFICADO",
        "ruv": "r1",
    }


@respx.mock
async def test_notify_identity_result_swallows_downstream_failures(adapter):
    """A failure to reach the notifications service does not raise."""
    respx.post(f"{BASE}/notify").mock(side_effect=httpx.ConnectError("boom"))

    await adapter.notify_identity_result(
        user_id="u1",
        email="john@example.com",
        full_name=None,
        status="NO_VERIFICADO",
        ruv="r1",
    )
