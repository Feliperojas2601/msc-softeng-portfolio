from datetime import UTC

import httpx
import pytest
import respx

from adapters.http.client import parse_datetime, request
from errors import DownstreamUnavailableError

URL = "http://svc.test/thing"


def test_parse_datetime_assumes_utc_when_naive():
    """A timestamp without offset is read as UTC."""
    assert parse_datetime("2026-01-01T00:00:00").tzinfo == UTC


def test_parse_datetime_keeps_explicit_offset():
    """A timestamp with an offset keeps its timezone."""
    parsed = parse_datetime("2026-01-01T00:00:00+00:00")
    assert parsed.utcoffset().total_seconds() == 0


@respx.mock
async def test_request_returns_http_responses_untouched():
    """Even a 500 response is handed back, not raised."""
    respx.get(URL).mock(return_value=httpx.Response(500))

    response = await request("GET", URL, timeout=1.0, max_retries=1)

    assert response.status_code == 500


@respx.mock
async def test_request_does_not_retry_non_get():
    """A POST is attempted exactly once on transport failure."""
    route = respx.post(URL).mock(side_effect=httpx.ConnectError("boom"))

    with pytest.raises(DownstreamUnavailableError):
        await request("POST", URL, timeout=1.0, max_retries=3)
    assert route.call_count == 1
