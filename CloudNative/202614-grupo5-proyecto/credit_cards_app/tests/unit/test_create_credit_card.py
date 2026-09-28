from datetime import datetime

import httpx
import pytest
from sqlalchemy import text

from domain.ports.payment_provider_port import PaymentTokenizationResult
from errors import (
    DuplicateCardError,
    ExpiredCardError,
    PaymentProviderRejectedError,
    PaymentProviderUnavailableError,
)

AUTH = {"Authorization": "Bearer session-token"}
BODY = {
    "cardNumber": "4111111111111111",
    "cvv": "123",
    "expirationDate": "99/12",
    "cardHolderName": "Ada Lovelace",
}


class FakePaymentProvider:
    def __init__(self, result=None, error=None):
        self.result = result or PaymentTokenizationResult("token-1", "VISA", "ruv-1")
        self.error = error
        self.calls = []

    def tokenize(self, **payload):
        self.calls.append(payload)
        if self.error:
            raise self.error
        return self.result


def make_provider(app, result=None, error=None):
    provider = FakePaymentProvider(result=result, error=error)
    app.extensions["credit_cards_payment_provider"] = provider
    return provider


def test_create_persists_only_allowed_card_data_and_returns_contract(
    client, app, database, users_response
):
    provider = make_provider(app)

    response = client.post("/credit-cards", headers=AUTH, json=BODY)

    assert response.status_code == 201
    assert set(response.json) == {"id", "userId", "createdAt"}
    assert response.json["userId"] == "owner-1"
    created_at = datetime.fromisoformat(response.json["createdAt"])
    assert created_at.tzinfo is not None
    assert provider.calls == [
        {
            "card_number": BODY["cardNumber"],
            "cvv": BODY["cvv"],
            "expiration_date": BODY["expirationDate"],
            "card_holder_name": BODY["cardHolderName"],
        }
    ]
    with database() as session:
        row = session.execute(
            text(
                "SELECT token, user_id, last_four_digits, issuer, status, ruv "
                "FROM credit_cards"
            )
        ).one()
    assert row == ("token-1", "owner-1", "1111", "VISA", "POR_VERIFICAR", "ruv-1")
    assert client.get("/credit-cards", headers=AUTH).json[0]["token"] == "token-1"


def test_create_uses_provider_franchise_and_allows_missing_initial_ruv(
    client, app, database
):
    make_provider(
        app,
        PaymentTokenizationResult("token-2", "AMERICAN_EXPRESS", None),
    )

    response = client.post("/credit-cards", headers=AUTH, json=BODY)

    assert response.status_code == 201
    with database() as session:
        row = session.execute(text("SELECT issuer, ruv FROM credit_cards")).one()
    assert row == ("AMERICAN EXPRESS", None)


@pytest.mark.parametrize(
    "body",
    [
        {},
        {**BODY, "cardNumber": "4111 1111 1111 1111"},
        {**BODY, "cardNumber": "abc"},
        {**BODY, "cvv": "12"},
        {**BODY, "expirationDate": "2029/12"},
        {**BODY, "expirationDate": "99/13"},
        {**BODY, "cardHolderName": "   "},
        {**BODY, "cardHolderName": None},
    ],
)
def test_invalid_body_returns_400_without_calling_dependencies(client, app, body):
    provider = make_provider(app)

    response = client.post("/credit-cards", headers=AUTH, json=body)

    assert response.status_code == 400
    assert response.data == b""
    assert provider.calls == []


@pytest.mark.parametrize("header", [None, "", "Bearer", "Basic abc", "Bearer a b"])
def test_create_authentication_status_codes(client, app, header):
    provider = make_provider(app)
    headers = {} if header is None else {"Authorization": header}

    response = client.post("/credit-cards", headers=headers, json=BODY)

    expected = 403 if header in (None, "", "Bearer") else 401
    assert response.status_code == expected
    assert provider.calls == []


def test_expired_card_returns_412_without_provider_call(client, app):
    provider = make_provider(app)
    body = {**BODY, "expirationDate": "20/01"}

    response = client.post("/credit-cards", headers=AUTH, json=body)

    assert response.status_code == 412
    assert provider.calls == []


@pytest.mark.parametrize(
    "error, status", [(DuplicateCardError(), 409), (ExpiredCardError(), 412)]
)
def test_provider_business_conflicts_are_translated(client, app, error, status):
    make_provider(app, error=error)

    response = client.post("/credit-cards", headers=AUTH, json=BODY)

    assert response.status_code == status
    assert response.data == b""


@pytest.mark.parametrize(
    "error", [PaymentProviderRejectedError(), PaymentProviderUnavailableError()]
)
def test_provider_failures_do_not_create_card(client, app, database, error):
    make_provider(app, error=error)

    response = client.post("/credit-cards", headers=AUTH, json=BODY)

    expected_status = 400 if isinstance(error, PaymentProviderRejectedError) else 503
    assert response.status_code == expected_status
    with database() as session:
        assert session.execute(text("SELECT COUNT(*) FROM credit_cards")).scalar() == 0


def test_duplicate_token_for_same_user_returns_409(client, app, seed_card):
    seed_card()
    make_provider(app, PaymentTokenizationResult("payment-token-card-1", "VISA", "r1"))

    response = client.post("/credit-cards", headers=AUTH, json=BODY)

    assert response.status_code == 409


def test_create_database_failure_returns_503(client, app, database):
    make_provider(app)
    from adapters.database.base import Base

    Base.metadata.drop_all(database.kw["bind"])

    response = client.post("/credit-cards", headers=AUTH, json=BODY)

    assert response.status_code == 503


@pytest.mark.parametrize(
    "response, expected",
    [
        (httpx.Response(409), DuplicateCardError),
        (httpx.Response(412), ExpiredCardError),
        (httpx.Response(400), PaymentProviderRejectedError),
        (httpx.Response(500), PaymentProviderUnavailableError),
        (httpx.Response(201, json={"token": "t"}), PaymentTokenizationResult),
    ],
)
def test_payment_adapter_translates_true_native_responses(
    monkeypatch, response, expected
):
    from adapters.http.payment_provider_adapter import HttpPaymentProviderAdapter

    monkeypatch.setattr(httpx, "post", lambda *args, **kwargs: response)
    adapter = HttpPaymentProviderAdapter("http://native", "secret", 2)

    if expected is PaymentTokenizationResult:
        result = adapter.tokenize(
            card_number=BODY["cardNumber"],
            cvv=BODY["cvv"],
            expiration_date=BODY["expirationDate"],
            card_holder_name=BODY["cardHolderName"],
        )
        assert result.token == "t"
    else:
        with pytest.raises(expected):
            adapter.tokenize(
                card_number=BODY["cardNumber"],
                cvv=BODY["cvv"],
                expiration_date=BODY["expirationDate"],
                card_holder_name=BODY["cardHolderName"],
            )
