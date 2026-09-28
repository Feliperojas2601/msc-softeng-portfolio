import httpx
import pytest
from sqlalchemy import text

from adapters.database.base import Base
from domain.models.credit_card import CreditCardStatus

AUTH = {"Authorization": "Bearer session-token"}


def test_list_returns_only_authenticated_users_cards(client, seed_card, users_response):
    seed_card("card-2", "owner-1", CreditCardStatus.APROBADA)
    seed_card("card-1", "owner-1", CreditCardStatus.RECHAZADA)
    seed_card("other-card", "owner-2")

    response = client.get("/credit-cards?userId=owner-2", headers=AUTH)

    assert response.status_code == 200
    assert response.json == [
        {
            "id": card_id,
            "token": f"payment-token-{card_id}",
            "userId": "owner-1",
            "lastFourDigits": "1234",
            "issuer": "VISA",
            "status": status,
            "createdAt": "2026-01-01T12:30:00",
            "updatedAt": "2026-01-02T13:40:00",
        }
        for card_id, status in [("card-1", "RECHAZADA"), ("card-2", "APROBADA")]
    ]
    assert users_response[1] == [
        (
            "http://users.test/users/me",
            {
                "headers": AUTH,
                "timeout": 1.5,
                "follow_redirects": False,
            },
        )
    ]


def test_pending_card_and_unknown_owner(client, seed_card, users_response):
    seed_card()
    assert (
        client.get("/credit-cards", headers=AUTH).json[0]["status"] == "POR_VERIFICAR"
    )
    users_response[0]["response"] = httpx.Response(200, json={"id": "another-owner"})
    assert client.get("/credit-cards", headers=AUTH).json == []


def test_empty_list(client):
    response = client.get("/credit-cards", headers=AUTH)
    assert response.status_code == 200
    assert response.json == []


@pytest.mark.parametrize("header", [None, "", "   ", "Bearer", "Bearer   "])
def test_missing_token_is_403(client, header, users_response):
    headers = {} if header is None else {"Authorization": header}
    response = client.get("/credit-cards", headers=headers)
    assert response.status_code == 403
    assert response.data == b""
    assert users_response[1] == []


@pytest.mark.parametrize(
    "header",
    [
        "Basic abc",
        "Bearer one two",
        "invalid",
        "Bearer inválido",
        "Bearer bad\x00token",
    ],
)
def test_malformed_authorization_is_401(client, header, users_response):
    response = client.get("/credit-cards", headers={"Authorization": header})
    assert response.status_code == 401
    assert response.data == b""
    assert users_response[1] == []


def test_bearer_scheme_is_case_insensitive(client):
    assert (
        client.get(
            "/credit-cards", headers={"Authorization": "bearer token"}
        ).status_code
        == 200
    )


@pytest.mark.parametrize("status", [401, 403])
def test_invalid_expired_or_unverified_token_is_401(client, users_response, status):
    users_response[0]["response"] = httpx.Response(status)
    response = client.get("/credit-cards", headers=AUTH)
    assert response.status_code == 401
    assert response.data == b""


@pytest.mark.parametrize(
    "upstream",
    [
        httpx.Response(500),
        httpx.Response(302, headers={"Location": "http://other.test"}),
        httpx.Response(200, text="not-json"),
        httpx.Response(200, json=[]),
        httpx.Response(200, json={}),
        httpx.Response(200, json={"id": 123}),
        httpx.Response(200, json={"id": "  "}),
        httpx.ReadTimeout("timeout"),
        httpx.ConnectError("unavailable"),
    ],
)
def test_users_failure_is_503_without_leaking_details(client, users_response, upstream):
    users_response[0]["response"] = upstream
    response = client.get("/credit-cards", headers=AUTH)
    assert response.status_code == 503
    assert response.data == b""


def test_authentication_precedes_database_access(client, database, users_response):
    Base.metadata.drop_all(database.kw["bind"])
    users_response[0]["response"] = httpx.Response(401)
    assert client.get("/credit-cards", headers=AUTH).status_code == 401


def test_count_includes_all_owners_without_auth(client, seed_card, users_response):
    assert client.get("/credit-cards/count").json == {"count": 0}
    seed_card()
    seed_card("card-2", "owner-2")
    response = client.get("/credit-cards/count")
    assert response.status_code == 200
    assert response.json == {"count": 2}
    assert users_response[1] == []


def test_reset_is_global_idempotent_and_preserves_other_tables(
    client, database, seed_card, users_response
):
    seed_card()
    seed_card("card-2", "owner-2")
    with database.begin() as session:
        session.execute(text("CREATE TABLE unrelated (id INTEGER PRIMARY KEY)"))
        session.execute(text("INSERT INTO unrelated (id) VALUES (1)"))

    for _ in range(2):
        response = client.post("/credit-cards/reset")
        assert response.status_code == 200
        assert response.json == {"msg": "Todos los datos fueron eliminados"}
        assert client.get("/credit-cards/count").json == {"count": 0}
    assert users_response[1] == []
    with database() as session:
        assert session.scalar(text("SELECT COUNT(*) FROM unrelated")) == 1
    assert client.get("/credit-cards", headers=AUTH).json == []


@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("get", "/credit-cards"),
        ("get", "/credit-cards/count"),
        ("post", "/credit-cards/reset"),
    ],
)
def test_database_failure_returns_503(client, database, method, path):
    Base.metadata.drop_all(database.kw["bind"])
    response = getattr(client, method)(path, headers=AUTH)
    assert response.status_code == 503
    assert response.data == b""
    assert client.get("/credit-cards/ping").data == b"pong"


def test_ping_does_not_require_dependencies(client, database, users_response):
    Base.metadata.drop_all(database.kw["bind"])
    users_response[0]["response"] = httpx.ConnectError("unavailable")
    response = client.get("/credit-cards/ping")
    assert response.status_code == 200
    assert response.mimetype == "text/plain"
    assert response.data == b"pong"
    assert users_response[1] == []


def test_internal_verification_requires_service_secret(client, app, seed_card):
    seed_card()
    app.config["CREDIT_CARDS_INTERNAL_SECRET"] = "service-secret"
    assert client.patch(
        "/credit-cards/internal/card-1/verification",
        json={"status": "APROBADA"},
    ).status_code == 403
    assert client.patch(
        "/credit-cards/internal/card-1/verification",
        headers={"Authorization": "Bearer wrong"},
        json={"status": "APROBADA"},
    ).status_code == 401


def test_internal_verification_is_idempotent(client, app, seed_card):
    card = seed_card()
    app.config["CREDIT_CARDS_INTERNAL_SECRET"] = "service-secret"
    headers = {"Authorization": "Bearer service-secret"}
    first = client.patch(
        f"/credit-cards/internal/{card.id}/verification",
        headers=headers,
        json={"status": "APROBADA", "eventId": "event-1"},
    )
    second = client.patch(
        f"/credit-cards/internal/{card.id}/verification",
        headers=headers,
        json={"status": "APROBADA", "eventId": "event-1"},
    )
    assert first.status_code == second.status_code == 200
    assert first.json == second.json
    assert second.json["status"] == "APROBADA"


def test_internal_verification_rejects_conflicting_terminal_state(
    client, app, seed_card
):
    card = seed_card()
    app.config["CREDIT_CARDS_INTERNAL_SECRET"] = "service-secret"
    headers = {"Authorization": "Bearer service-secret"}
    client.patch(
        f"/credit-cards/internal/{card.id}/verification",
        headers=headers,
        json={"status": "APROBADA"},
    )
    response = client.patch(
        f"/credit-cards/internal/{card.id}/verification",
        headers=headers,
        json={"status": "RECHAZADA"},
    )
    assert response.status_code == 409
