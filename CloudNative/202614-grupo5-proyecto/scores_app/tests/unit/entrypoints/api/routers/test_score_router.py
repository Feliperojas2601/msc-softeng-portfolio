from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from assembly import build_create_score_use_case, build_get_score_use_case
from entrypoints.api.main import app
from errors import InvalidScoreError, ScoreNotFoundError


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


def test_ping_returns_pong(client):
    """GET /scores/ping is a plain healthcheck."""
    response = client.get("/scores/ping")

    assert response.status_code == 200
    assert response.text == "pong"


def test_create_score_success(client, existing_score, valid_score_data):
    """POST /scores returns 201 with the calculated utility on success."""
    use_case = AsyncMock()
    use_case.execute.return_value = existing_score
    _override(build_create_score_use_case, use_case)

    response = client.post("/scores", json=valid_score_data)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == existing_score.id
    assert body["utility"] == existing_score.utility


def test_create_score_missing_field_returns_400(client, valid_score_data):
    """POST /scores returns 400 when required fields are missing or invalid."""
    del valid_score_data["offer"]

    response = client.post("/scores", json=valid_score_data)

    assert response.status_code == 400


def test_create_score_invalid_size_returns_412(client, valid_score_data):
    """POST /scores returns 412 when the size is not LARGE, MEDIUM or SMALL."""
    use_case = AsyncMock()
    use_case.execute.side_effect = InvalidScoreError("El tamaño 'XLARGE' no es válido")
    _override(build_create_score_use_case, use_case)

    response = client.post("/scores", json={**valid_score_data, "size": "XLARGE"})

    assert response.status_code == 412
    assert response.json()["msg"] == "El tamaño 'XLARGE' no es válido"


def test_get_score_by_offer_id_success(client, existing_score):
    """GET /scores/{offerId} returns 200 with the score when it exists."""
    use_case = AsyncMock()
    use_case.execute.return_value = existing_score
    _override(build_get_score_use_case, use_case)

    response = client.get(f"/scores/{existing_score.offerId}")

    assert response.status_code == 200
    assert response.json()["utility"] == existing_score.utility


def test_get_score_by_offer_id_returns_404_when_missing(client):
    """GET /scores/{offerId} returns 404 when the offer has no score yet."""
    use_case = AsyncMock()
    use_case.execute.side_effect = ScoreNotFoundError()
    _override(build_get_score_use_case, use_case)

    response = client.get("/scores/offer-without-score")

    assert response.status_code == 404
