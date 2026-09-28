from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from assembly import (
    build_count_offers_use_case,
    build_create_offer_use_case,
    build_delete_offer_use_case,
    build_get_offer_by_id_use_case,
    build_get_offer_filter_use_case,
    build_reset_offers_use_case,
)
from entrypoints.api.main import app
from errors import InvalidOfferError, OfferNotFoundError


@pytest.fixture
def client():
    """Fixture providing a TestClient that never runs the app's lifespan (no real DB)."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_overrides():
    """Ensure dependency overrides never leak between tests."""
    yield
    app.dependency_overrides.clear()


def _override(builder, use_case):
    app.dependency_overrides[builder] = lambda: use_case


def test_create_offer_success(client, existing_offer, valid_offer_data):
    """POST /offers returns 201 with id, userId, and createdAt on success."""
    use_case = AsyncMock()
    use_case.execute.return_value = existing_offer
    _override(build_create_offer_use_case, use_case)

    response = client.post("/offers", json=valid_offer_data)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == existing_offer.id
    assert body["userId"] == existing_offer.userId
    assert "createdAt" in body


def test_create_offer_missing_field_returns_400(client, valid_offer_data):
    """POST /offers returns 400 when required fields are missing or invalid."""
    del valid_offer_data["description"]

    response = client.post("/offers", json=valid_offer_data)

    assert response.status_code == 400


def test_create_offer_invalid_size_returns_412(client, valid_offer_data):
    """POST /offers returns 412 when the size is not LARGE, MEDIUM or SMALL."""
    use_case = AsyncMock()
    use_case.execute.side_effect = InvalidOfferError("El tamaño 'XLARGE' no es válido")
    _override(build_create_offer_use_case, use_case)

    response = client.post("/offers", json={**valid_offer_data, "size": "XLARGE"})

    assert response.status_code == 412
    assert response.json()["msg"] == "El tamaño 'XLARGE' no es válido"


def test_create_offer_negative_value_returns_412(client, valid_offer_data):
    """POST /offers returns 412 when the offer value is negative."""
    use_case = AsyncMock()
    use_case.execute.side_effect = InvalidOfferError(
        "El valor de la oferta no puede ser negativo"
    )
    _override(build_create_offer_use_case, use_case)

    response = client.post("/offers", json={**valid_offer_data, "offer": -1})

    assert response.status_code == 412


def test_get_all_offers_without_filters(client, existing_offer, existing_offer_2):
    """GET /offers returns all offers when no query parameters are passed."""
    use_case = AsyncMock()
    use_case.execute.return_value = [existing_offer, existing_offer_2]
    _override(build_get_offer_filter_use_case, use_case)

    response = client.get("/offers")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert body[0]["id"] == existing_offer.id
    assert body[1]["id"] == existing_offer_2.id


def test_get_all_offers_with_query_filters(client, existing_offer):
    """GET /offers applies query filters and returns matching records."""
    use_case = AsyncMock()
    use_case.execute.return_value = [existing_offer]
    _override(build_get_offer_filter_use_case, use_case)

    response = client.get(
        f"/offers?post={existing_offer.postId}&owner={existing_offer.userId}"
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == existing_offer.id
    use_case.execute.assert_awaited_once()


def test_get_offer_by_id_success(client, existing_offer):
    """GET /offers/{id} returns offer object when found."""
    use_case = AsyncMock()
    use_case.execute.return_value = existing_offer
    _override(build_get_offer_by_id_use_case, use_case)

    response = client.get(f"/offers/{existing_offer.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == existing_offer.id
    assert body["postId"] == existing_offer.postId
    assert body["userId"] == existing_offer.userId


def test_get_offer_by_id_invalid_uuid_returns_400(client):
    """GET /offers/{id} returns 400 if id path parameter is not a valid UUID."""
    response = client.get("/offers/not-a-valid-uuid")
    assert response.status_code == 400


def test_get_offer_by_id_not_found_returns_404(client):
    """GET /offers/{id} returns 404 when offer does not exist."""
    use_case = AsyncMock()
    use_case.execute.side_effect = OfferNotFoundError()
    _override(build_get_offer_by_id_use_case, use_case)

    response = client.get("/offers/a1b2c3d4-1111-4000-8000-000000000099")
    assert response.status_code == 404


def test_delete_offer_success(client, existing_offer):
    """DELETE /offers/{id} removes offer and returns confirmation message."""
    use_case = AsyncMock()
    use_case.execute.return_value = True
    _override(build_delete_offer_use_case, use_case)

    response = client.delete(f"/offers/{existing_offer.id}")

    assert response.status_code == 200
    assert response.json() == {"msg": "la oferta fue eliminada"}


def test_delete_offer_invalid_uuid_returns_400(client):
    """DELETE /offers/{id} returns 400 when id is not a valid UUID."""
    response = client.delete("/offers/invalid-uuid-format")
    assert response.status_code == 400


def test_delete_offer_not_found_returns_404(client):
    """DELETE /offers/{id} returns 404 when target offer does not exist."""
    use_case = AsyncMock()
    use_case.execute.side_effect = OfferNotFoundError()
    _override(build_delete_offer_use_case, use_case)

    response = client.delete("/offers/a1b2c3d4-1111-4000-8000-000000000099")
    assert response.status_code == 404


def test_count_offers_success(client):
    """GET /offers/count returns total integer count."""
    use_case = AsyncMock()
    use_case.execute.return_value = 5
    _override(build_count_offers_use_case, use_case)

    response = client.get("/offers/count")

    assert response.status_code == 200
    assert response.json() == {"count": 5}


def test_ping_success(client):
    """GET /offers/ping returns plain text 'pong'."""
    response = client.get("/offers/ping")

    assert response.status_code == 200
    assert response.text == "pong"


def test_reset_offers_success(client):
    """POST /offers/reset wipes all offers and returns confirmation message."""
    use_case = AsyncMock()
    use_case.execute.return_value = None
    _override(build_reset_offers_use_case, use_case)

    response = client.post("/offers/reset")

    assert response.status_code == 200
    assert response.json() == {"msg": "las ofertas fueron eliminadas"}
