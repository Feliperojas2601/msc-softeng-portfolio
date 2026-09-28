import importlib.util
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest
from sqlalchemy import select

import adapters.database.credit_card_repository as cards_repository
import adapters.database.verification_outbox as outbox
import domain.use_cases.create_credit_card_use_case as create_card
from domain.ports.payment_provider_port import PaymentTokenizationResult

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "timing_mediator", ROOT / "credit_cards_mediator_app/src/handler.py"
)
mediator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mediator
spec.loader.exec_module(mediator)
AUTH = {"Authorization": "Bearer service-secret"}
USER_AUTH = {"Authorization": "Bearer test-user-token"}
EVENTS = "/credit-cards/internal/verification-events"


@pytest.fixture
def clock(monkeypatch, app):
    class Clock(datetime):
        second = 0

        @classmethod
        def now(cls, tz=None):
            return datetime(2026, 9, 25, tzinfo=UTC) + timedelta(seconds=cls.second)

    monkeypatch.setattr(outbox, "datetime", Clock)
    monkeypatch.setattr(cards_repository, "datetime", Clock)
    monkeypatch.setattr(create_card, "datetime", Clock)
    app.config["CREDIT_CARDS_INTERNAL_SECRET"] = "service-secret"
    return Clock


def claim(client):
    response = client.post(f"{EVENTS}/claim", headers=AUTH)
    assert response.status_code == 200
    return response.json


@pytest.mark.parametrize("target", ["APROBADA", "RECHAZADA"])
@pytest.mark.parametrize("start", [0, 1.5])
def test_created_card_reaches_terminal_state_before_evaluator_query(
    client, app, database, clock, target, start
):
    app.extensions["credit_cards_payment_provider"] = SimpleNamespace(
        tokenize=lambda **kwargs: PaymentTokenizationResult("token", "VISA", "ruv")
    )
    created = client.post(
        "/credit-cards",
        headers=USER_AUTH,
        json={
            "cardNumber": "4111111111111111",
            "cvv": "123",
            "expirationDate": "99/12",
            "cardHolderName": "Test User",
        },
    )
    assert created.status_code == 201
    assert set(created.json) == {"id", "userId", "createdAt"}
    assert (
        client.get("/credit-cards", headers=USER_AUTH).json[0]["status"]
        == "POR_VERIFICAR"
    )
    settings = mediator.Settings(
        "http://native",
        "native-secret",
        "http://cards",
        "service-secret",
        "http://users",
        "http://notify",
    )
    phase = "ACCEPTED"
    poll_times = []
    notifications = []

    def request(method, url, token, payload, timeout):
        nonlocal phase
        if url.startswith("http://cards"):
            response = client.open(
                url.removeprefix("http://cards"),
                method=method,
                json=payload,
                headers={"Authorization": f"Bearer {token}"},
            )
            return mediator.HttpResponse(response.status_code, response.json)
        if url.startswith("http://native"):
            poll_times.append(clock.second)
            if phase == "PROCESSED":
                return mediator.HttpResponse(200, {"status": target})
            if phase == "ACCEPTED":
                phase = "PENDING"
            elif clock.second >= 5:
                phase = "PROCESSED"
            return mediator.HttpResponse(202, {})
        if url.startswith("http://users"):
            return mediator.HttpResponse(
                200, {"id": "owner-1", "email": "test@example.com"}
            )
        assert url == "http://notify/notify"
        notifications.append(payload)
        return mediator.HttpResponse(200, {"msg": "ok"})

    for cycle in range(5):
        clock.second = start + cycle * 2
        for event in mediator.claim_events(settings, request):
            mediator.process_event(event, settings, request)
    clock.second = 10
    response = client.get("/credit-cards", headers=USER_AUTH)
    assert response.status_code == 200
    assert response.json[0]["id"] == created.json["id"]
    assert response.json[0]["status"] == target
    assert datetime.fromisoformat(
        response.json[0]["updatedAt"]
    ) > datetime.fromisoformat(response.json[0]["createdAt"])
    assert len(notifications) == 1
    assert notifications[0]["status"] == (
        "VERIFICADA" if target == "APROBADA" else target
    )
    assert poll_times[-1] < 10
    assert claim(client) == []
    with database() as session:
        row = session.scalar(select(outbox.VerificationOutboxModel))
        assert row.published_at is not None


def test_release_reschedules_without_finishing_and_rejects_old_lease(
    client, seed_card, clock
):
    seed_card()
    event = claim(client)[0]
    assert claim(client) == []
    url = f"{EVENTS}/{event['eventId']}/release"
    assert client.post(url, headers=AUTH, json={"leaseId": "wrong"}).status_code == 409
    response = client.post(url, headers=AUTH, json={"leaseId": event["leaseId"]})
    assert response.status_code == 200
    assert response.json == {"scheduled": True}
    assert claim(client) == []
    clock.second = 1
    reclaimed = claim(client)[0]
    assert reclaimed["leaseId"] != event["leaseId"]
    assert (
        client.post(url, headers=AUTH, json={"leaseId": event["leaseId"]}).status_code
        == 409
    )
    assert (
        client.post(
            f"{EVENTS}/{event['eventId']}/ack",
            headers=AUTH,
            json={"leaseId": event["leaseId"]},
        ).status_code
        == 409
    )
    assert (
        client.get("/credit-cards", headers=USER_AUTH).json[0]["status"]
        == "POR_VERIFICAR"
    )


def test_worker_crash_releases_event_only_after_lease_expires(client, seed_card, clock):
    seed_card()
    event = claim(client)[0]
    clock.second = outbox.PROCESSING_LEASE_SECONDS - 1
    assert claim(client) == []
    clock.second = outbox.PROCESSING_LEASE_SECONDS
    assert (
        client.post(
            f"{EVENTS}/{event['eventId']}/release",
            headers=AUTH,
            json={"leaseId": event["leaseId"]},
        ).status_code
        == 409
    )
    reclaimed = claim(client)[0]
    assert reclaimed["eventId"] == event["eventId"]
    assert reclaimed["leaseId"] != event["leaseId"]


def test_completed_event_cannot_be_released(client, seed_card, clock):
    seed_card()
    event = claim(client)[0]
    body = {"leaseId": event["leaseId"]}
    assert (
        client.post(
            f"{EVENTS}/{event['eventId']}/ack", headers=AUTH, json=body
        ).status_code
        == 200
    )
    assert (
        client.post(
            f"{EVENTS}/{event['eventId']}/release", headers=AUTH, json=body
        ).status_code
        == 409
    )
    clock.second = 120
    assert claim(client) == []


@pytest.mark.parametrize("headers,status", [({}, 403), (USER_AUTH, 401)])
def test_release_requires_service_credentials(
    client, seed_card, clock, headers, status
):
    seed_card()
    event = claim(client)[0]
    assert (
        client.post(
            f"{EVENTS}/{event['eventId']}/release",
            headers=headers,
            json={"leaseId": event["leaseId"]},
        ).status_code
        == status
    )
    assert claim(client) == []


@pytest.mark.parametrize("body", [None, {}, {"leaseId": 42}, {"leaseId": ""}])
def test_release_validates_lease_body(client, clock, body):
    assert (
        client.post(f"{EVENTS}/event/release", headers=AUTH, json=body).status_code
        == 400
    )


def test_claim_reserves_only_one_event_per_serial_worker(client, seed_card, clock):
    seed_card(card_id="first")
    seed_card(card_id="second")
    first = claim(client)
    second = claim(client)
    assert len(first) == len(second) == 1
    assert first[0]["cardId"] != second[0]["cardId"]
