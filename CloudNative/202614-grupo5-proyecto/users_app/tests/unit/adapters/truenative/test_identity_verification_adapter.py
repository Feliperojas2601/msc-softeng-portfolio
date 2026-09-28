import json

import httpx
import pytest
import respx

from adapters.truenative.identity_verification_adapter import (
    TrueNativeIdentityVerificationAdapter,
)
from errors import IdentityVerificationRequestError

BASE = "http://true-native.test"
VERIFY_URL = f"{BASE}/native/verify"


@pytest.fixture
def adapter() -> TrueNativeIdentityVerificationAdapter:
    """A TrueNative adapter pointed at the mocked base URL."""
    return TrueNativeIdentityVerificationAdapter(BASE, secret_token="s3cr3t")


@respx.mock
async def test_request_verification_sends_expected_payload_and_headers(adapter):
    """The request body and Authorization header match TrueNative's contract."""
    route = respx.post(VERIFY_URL).mock(
        return_value=httpx.Response(201, json={"RUV": "r1", "task_status": "ACCEPTED"})
    )

    await adapter.request_verification(
        user_id="u1",
        transaction_identifier="t1",
        webhook_url="https://example.com/callback",
        email="john@example.com",
        dni="123",
        full_name="John Doe",
        phone_number="3000000000",
    )

    sent = route.calls.last.request
    assert sent.headers["Authorization"] == "Bearer s3cr3t"
    payload = json.loads(sent.content)
    assert payload["userIdentifier"] == "u1"
    assert payload["transactionIdentifier"] == "t1"
    assert payload["userWebhook"] == "https://example.com/callback"
    assert payload["user"] == {
        "email": "john@example.com",
        "dni": "123",
        "fullName": "John Doe",
        "phone": "3000000000",
    }


@respx.mock
async def test_request_verification_raises_on_non_201(adapter):
    """A non-201 response is surfaced as IdentityVerificationRequestError."""
    respx.post(VERIFY_URL).mock(return_value=httpx.Response(409))

    with pytest.raises(IdentityVerificationRequestError):
        await adapter.request_verification(
            user_id="u1",
            transaction_identifier="t1",
            webhook_url="https://example.com/callback",
            email="john@example.com",
        )


@respx.mock
async def test_request_verification_raises_on_transport_error(adapter):
    """A network failure is surfaced as IdentityVerificationRequestError."""
    respx.post(VERIFY_URL).mock(side_effect=httpx.ConnectError("boom"))

    with pytest.raises(IdentityVerificationRequestError):
        await adapter.request_verification(
            user_id="u1",
            transaction_identifier="t1",
            webhook_url="https://example.com/callback",
            email="john@example.com",
        )
