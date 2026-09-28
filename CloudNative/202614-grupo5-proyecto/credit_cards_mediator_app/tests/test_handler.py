import pytest

import handler as module
from handler import (
    HttpResponse,
    InternalApiError,
    InvalidMessageError,
    NotificationError,
    PollingError,
    ProviderResponseError,
    Settings,
    process_event,
)


@pytest.fixture
def settings():
    return Settings(
        "https://native.test",
        "native-secret",
        "https://cards.test",
        "cards-secret",
        "https://users.test",
        "http://notifications-app-service",
    )


def verification_event(payload=None, event_id="event-1"):
    return payload or {
        "cardId": "card-1",
        "ruv": "ruv-1",
        "eventId": event_id,
        "leaseId": "lease-1",
    }


def card(status="POR_VERIFICAR"):
    return {
        "id": "card-1",
        "userId": "owner-1",
        "ruv": "ruv-1",
        "status": status,
        "lastFourDigits": "1234",
        "franchise": "VISA",
        "updatedAt": "2026-01-01T00:00:00",
    }


class Services:
    def __init__(self, status="POR_VERIFICAR", native_status=200, result="APPROVED"):
        self.card = card(status)
        self.native = HttpResponse(native_status, {"status": result})
        self.user = HttpResponse(
            200, {"id": "owner-1", "email": "owner@example.com", "fullName": "Ada"}
        )
        self.notify = HttpResponse(200, {"msg": "ok"})
        self.patch_code = 200
        self.ack_code = 200
        self.release_code = 200
        self.calls = []

    def __call__(self, method, url, token, payload, timeout):
        self.calls.append((method, url, token, payload))
        if url.endswith("/ack"):
            return HttpResponse(self.ack_code, {"published": self.ack_code == 200})
        if url.endswith("/release"):
            return HttpResponse(self.release_code, {"scheduled": True})
        if url.startswith("https://cards.test"):
            if method == "PATCH":
                if self.patch_code != 200:
                    return HttpResponse(self.patch_code, None)
                self.card["status"] = payload["status"]
            return HttpResponse(200, dict(self.card))
        if url.startswith("https://native.test"):
            return self.native
        if url.startswith("https://users.test"):
            return self.user
        if url == "http://notifications-app-service/notify":
            if isinstance(self.notify, Exception):
                raise self.notify
            return self.notify
        raise AssertionError(url)


@pytest.mark.parametrize(
    "provider,stored,notified",
    [
        ("APPROVED", "APROBADA", "VERIFICADA"),
        ("REJECTED", "RECHAZADA", "RECHAZADA"),
    ],
)
def test_terminal_result_notifies_exact_contract(settings, provider, stored, notified):
    services = Services(result=provider)
    assert process_event(verification_event(), settings, services) == stored
    assert [call[0] for call in services.calls] == [
        "GET",
        "GET",
        "PATCH",
        "GET",
        "POST",
        "POST",
    ]
    notify_call = next(c for c in services.calls if c[1].endswith("/notify"))
    assert notify_call[2] == ""
    assert notify_call[3] == {
        "type": "CREDIT_CARD_VERIFICATION",
        "userId": "owner-1",
        "email": "owner@example.com",
        "fullName": "Ada",
        "status": notified,
        "ruv": "ruv-1",
        "lastFourDigits": "1234",
        "franchise": "VISA",
    }
    ack_call = services.calls[-1]
    assert ack_call[1].endswith("/verification-events/event-1/ack")
    assert ack_call[3] == {"leaseId": "lease-1"}
    assert services.card["status"] == stored


def test_pending_releases_event_without_ack(settings):
    services = Services(native_status=202)
    assert process_event(verification_event(), settings, services) == "PENDING"
    assert [c[0] for c in services.calls] == ["GET", "GET", "POST"]
    assert services.calls[-1][1].endswith("/verification-events/event-1/release")
    assert services.calls[-1][2] == settings.cards_api_secret
    assert services.calls[-1][3] == {"leaseId": "lease-1"}
    assert not any(c[1].endswith("/ack") for c in services.calls)


@pytest.mark.parametrize("code", [401, 409, 503])
def test_release_failure_keeps_card_pending(settings, code):
    services = Services(native_status=202)
    services.release_code = code
    with pytest.raises(InternalApiError):
        process_event(verification_event(), settings, services)
    assert services.card["status"] == "POR_VERIFICAR"
    assert not any(c[1].endswith(("/ack", "/notify")) for c in services.calls)


@pytest.mark.parametrize(
    "failure",
    [
        HttpResponse(502, None),
        ProviderResponseError("timeout"),
    ],
)
def test_failed_notification_retries_without_verification(settings, failure):
    services = Services()
    services.notify = failure
    with pytest.raises(PollingError):
        process_event(verification_event(), settings, services)
    assert services.card["status"] == "APROBADA"
    assert not any(c[1].endswith("/ack") for c in services.calls)
    services.notify = HttpResponse(200, {})
    services.calls.clear()
    assert process_event(verification_event(), settings, services) == "APROBADA"
    assert [c[0] for c in services.calls] == ["GET", "GET", "POST", "POST"]
    assert not any("/native/" in c[1] for c in services.calls)


@pytest.mark.parametrize("status", ["APROBADA", "RECHAZADA"])
def test_terminal_duplicate_does_not_repeat_patch(settings, status):
    services = Services(status=status)
    for _ in range(2):
        assert process_event(verification_event(), settings, services) == status
    assert all(c[0] != "PATCH" and "/native/" not in c[1] for c in services.calls)


@pytest.mark.parametrize(
    "response",
    [
        HttpResponse(503, None),
        HttpResponse(200, {}),
        HttpResponse(200, {"id": "other", "email": "other@example.com"}),
        HttpResponse(200, {"id": "owner-1", "email": ""}),
    ],
)
def test_missing_contact_is_retryable_and_never_sends(settings, response):
    services = Services()
    services.user = response
    with pytest.raises(NotificationError):
        process_event(verification_event(), settings, services)
    assert services.card["status"] == "APROBADA"
    assert not any(c[0] == "POST" for c in services.calls)


def test_optional_fields_can_be_absent(settings):
    services = Services(status="RECHAZADA")
    del services.user.body["fullName"]
    del services.card["lastFourDigits"]
    del services.card["franchise"]
    process_event(verification_event(), settings, services)
    notify_call = next(c for c in services.calls if c[1].endswith("/notify"))
    payload = notify_call[3]
    assert payload["fullName"] is None
    assert "franchise" not in payload
    assert "lastFourDigits" not in payload


@pytest.mark.parametrize("code", [400, 401, 409, 500, 503])
def test_patch_failure_prevents_notification(settings, code):
    services = Services()
    services.patch_code = code
    with pytest.raises(InternalApiError):
        process_event(verification_event(), settings, services)
    assert not any(c[0] == "POST" for c in services.calls)


def test_ack_failure_is_raised_after_successful_notification(settings):
    services = Services()
    services.ack_code = 500
    with pytest.raises(InternalApiError):
        process_event(verification_event(), settings, services)
    assert services.card["status"] == "APROBADA"
    assert any(c[1].endswith("/notify") for c in services.calls)


def test_provider_error_never_changes_state(settings):
    services = Services(native_status=503)
    with pytest.raises(ProviderResponseError):
        process_event(verification_event(), settings, services)
    assert services.card["status"] == "POR_VERIFICAR"


def test_unknown_provider_response_is_retryable(settings):
    services = Services(result="UNKNOWN")
    with pytest.raises(ProviderResponseError):
        process_event(verification_event(), settings, services)


@pytest.mark.parametrize(
    "payload",
    [
        {"ruv": "r", "eventId": "e", "leaseId": "l"},
        {"cardId": "c", "eventId": "e", "leaseId": "l"},
        {"cardId": "c", "ruv": "r", "leaseId": "l"},
        {"cardId": "c", "ruv": "r", "eventId": "e"},
    ],
)
def test_invalid_event(settings, payload):
    with pytest.raises(InvalidMessageError):
        process_event(verification_event(payload), settings, Services())


def test_wrong_ruv_does_not_query_provider_or_send(settings):
    services = Services()
    with pytest.raises(InternalApiError):
        process_event(
            verification_event(
                {"cardId": "card-1", "ruv": "wrong", "eventId": "e", "leaseId": "l"}
            ),
            settings,
            services,
        )
    assert len(services.calls) == 1


def test_claim_events_failure_raises(settings):
    def request_fn(method, url, token, payload, timeout):
        return HttpResponse(500, None)

    with pytest.raises(InternalApiError):
        module.claim_events(settings, request_fn)


def test_claim_events_returns_body(settings):
    events = [verification_event()]

    def request_fn(method, url, token, payload, timeout):
        assert method == "POST"
        assert url.endswith("/credit-cards/internal/verification-events/claim")
        assert token == "cards-secret"
        return HttpResponse(200, events)

    assert module.claim_events(settings, request_fn) == events


def test_run_once_reports_processed_and_failed(monkeypatch, settings):
    events = [
        verification_event(event_id="good"),
        verification_event(event_id="bad"),
    ]
    monkeypatch.setattr(module, "claim_events", lambda settings: events)

    def fake_process(event, settings):
        if event["eventId"] == "bad":
            raise ProviderResponseError("boom")
        return "APROBADA"

    monkeypatch.setattr(module, "process_event", fake_process)
    result = module.run_once(settings)
    assert result == (1, 1)


def test_env_requires_notification_configuration(monkeypatch):
    for key in (
        "TRUE_NATIVE_BASE_URL",
        "TRUE_NATIVE_SECRET_TOKEN",
        "CARDS_API_BASE_URL",
        "CARDS_API_SECRET",
        "USERS_API_BASE_URL",
    ):
        monkeypatch.setenv(key, "test")
    monkeypatch.delenv("NOTIFICATIONS_API_BASE_URL", raising=False)
    with pytest.raises(PollingError, match="notifications_api_base_url"):
        Settings.from_env()


def test_transport_does_not_forward_secret_on_redirect(monkeypatch):
    assert (
        module.NoRedirects().redirect_request(None, None, 302, "", {}, "https://other")
        is None
    )
    captured = []

    class Response:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def read(self):
            return b'{"msg": "ok"}'

    class Opener:
        def open(self, request, timeout):
            captured.append(request)
            return Response()

    monkeypatch.setattr(module, "build_opener", lambda *args: Opener())
    module.http_request("POST", "http://notifications-app-service/notify", "", {}, 1)
    assert not captured[0].has_header("Authorization")
