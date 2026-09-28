import importlib.util
import sys
from pathlib import Path

import pytest


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ROOT = Path(__file__).resolve().parents[3]
mediator = load_module(
    "cards_mediator_contract", ROOT / "credit_cards_mediator_app/src/handler.py"
)
schemas = load_module(
    "notification_contract",
    ROOT / "notifications_app/src/entrypoints/api/schemas/notify_schemas.py",
)
AUTH = {"Authorization": "Bearer service-secret"}


@pytest.mark.parametrize(
    "status,expected", [("APPROVED", "VERIFICADA"), ("REJECTED", "RECHAZADA")]
)
def test_polling_to_notification_contract_and_retry(
    client, app, seed_card, status, expected
):
    app.config["CREDIT_CARDS_INTERNAL_SECRET"] = "service-secret"
    seed_card()
    settings = mediator.Settings(
        "https://native.test",
        "native-secret",
        "https://cards.test",
        "service-secret",
        "https://users.test",
        "http://notifications-app-service",
    )
    calls = []
    payloads = []
    fail_notification = True

    def request(method, url, token, payload, timeout):
        calls.append((method, url))
        if url.endswith("/ack"):
            return mediator.HttpResponse(200, {"published": True})
        if url.startswith("https://cards.test"):
            response = client.open(
                url.removeprefix("https://cards.test"),
                method=method,
                json=payload,
                headers={"Authorization": f"Bearer {token}"},
            )
            return mediator.HttpResponse(response.status_code, response.json)
        if url.startswith("https://native.test"):
            return mediator.HttpResponse(200, {"status": status})
        if url.startswith("https://users.test"):
            assert url.endswith("/users/owner-1")
            return mediator.HttpResponse(
                200, {"id": "owner-1", "email": "ada@example.com", "fullName": None}
            )
        assert url == "http://notifications-app-service/notify"
        assert method == "POST" and token == ""
        parsed = schemas.NotifyRequest.model_validate(payload)
        assert parsed.type == "CREDIT_CARD_VERIFICATION"
        assert parsed.status == expected
        payloads.append(payload)
        return mediator.HttpResponse(502 if fail_notification else 200, {})

    event = {
        "cardId": "card-1",
        "ruv": "ruv-card-1",
        "eventId": "event-1",
        "leaseId": "lease-1",
    }
    with pytest.raises(mediator.NotificationError):
        mediator.process_event(event, settings, request)

    persisted = client.get(
        "/credit-cards/internal/card-1/verification", headers=AUTH
    ).json
    assert persisted["status"] == (
        "APROBADA" if expected == "VERIFICADA" else "RECHAZADA"
    )
    fail_notification = False
    calls.clear()
    mediator.process_event(event, settings, request)
    assert [method for method, _ in calls] == ["GET", "GET", "POST", "POST"]
    assert not any("/native/" in url for _, url in calls)
    assert (
        client.get("/credit-cards/internal/card-1/verification", headers=AUTH).json
        == persisted
    )
    assert payloads[0] == payloads[1]
    assert set(payloads[0]) == {
        "type",
        "userId",
        "email",
        "fullName",
        "status",
        "ruv",
        "lastFourDigits",
        "franchise",
    }
    assert payloads[0]["lastFourDigits"] == "1234"
    assert payloads[0]["franchise"] == "VISA"


def test_internal_read_returns_only_verification_metadata(client, app, seed_card):
    app.config["CREDIT_CARDS_INTERNAL_SECRET"] = "service-secret"
    seed_card()
    response = client.get("/credit-cards/internal/card-1/verification", headers=AUTH)
    assert response.status_code == 200
    assert set(response.json) == {
        "id",
        "userId",
        "ruv",
        "status",
        "lastFourDigits",
        "franchise",
        "updatedAt",
    }
    assert response.json["userId"] == "owner-1"
    assert (
        client.get(
            "/credit-cards/internal/missing/verification", headers=AUTH
        ).status_code
        == 404
    )


@pytest.mark.parametrize(
    "headers,code",
    [
        ({}, 403),
        ({"Authorization": "Bearer wrong"}, 401),
        ({"Authorization": "Bearer session-token"}, 401),
    ],
)
def test_internal_read_requires_service_auth(client, app, seed_card, headers, code):
    app.config["CREDIT_CARDS_INTERNAL_SECRET"] = "service-secret"
    seed_card()
    response = client.get("/credit-cards/internal/card-1/verification", headers=headers)
    assert response.status_code == code


def test_internal_read_disabled_without_secret(client, app):
    app.config["CREDIT_CARDS_INTERNAL_SECRET"] = ""
    assert (
        client.get(
            "/credit-cards/internal/card-1/verification", headers=AUTH
        ).status_code
        == 503
    )
