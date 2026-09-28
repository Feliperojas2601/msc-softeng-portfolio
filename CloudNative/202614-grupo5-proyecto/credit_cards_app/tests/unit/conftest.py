from datetime import UTC, datetime

import httpx
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from adapters.database.base import Base
from adapters.database.credit_card_repository import SQLAlchemyCreditCardRepository
from adapters.http.users_adapter import HttpUsersAdapter
from assembly import create_app
from domain.models.credit_card import CreditCard, CreditCardIssuer, CreditCardStatus


@pytest.fixture
def database():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield sessionmaker(bind=engine, expire_on_commit=False)
    engine.dispose()


@pytest.fixture
def users_response(monkeypatch):
    calls = []
    state = {"response": httpx.Response(200, json={"id": "owner-1"})}

    def get(url, **kwargs):
        calls.append((url, kwargs))
        if isinstance(state["response"], Exception):
            raise state["response"]
        return state["response"]

    monkeypatch.setattr(httpx, "get", get)
    return state, calls


@pytest.fixture
def app(database, users_response):
    app = create_app(database, HttpUsersAdapter("http://users.test/", 1.5))
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def seed_card(database):
    def seed(
        card_id="card-1", user_id="owner-1", status=CreditCardStatus.POR_VERIFICAR
    ):
        card = CreditCard(
            id=card_id,
            token=f"payment-token-{card_id}",
            user_id=user_id,
            last_four_digits="1234",
            ruv=f"ruv-{card_id}",
            issuer=CreditCardIssuer.VISA,
            status=status,
            created_at=datetime(2026, 1, 1, 12, 30, tzinfo=UTC),
            updated_at=datetime(2026, 1, 2, 13, 40, tzinfo=UTC),
        )
        with database() as session:
            SQLAlchemyCreditCardRepository(session).create(card)
        return card

    return seed
