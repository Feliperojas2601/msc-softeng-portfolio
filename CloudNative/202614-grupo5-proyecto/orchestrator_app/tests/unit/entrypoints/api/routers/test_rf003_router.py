from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from assembly import build_create_post_rf003_use_case
from domain.models.post import CreatedPostResponse, CreatedRouteSummary
from entrypoints.api.main import app
from errors import (
    DownstreamUnavailableError,
    DuplicatePostError,
    InvalidDatesError,
    InvalidExpirationDateError,
    InvalidTokenError,
    MissingTokenError,
)

AUTH = {"Authorization": "Bearer token"}


@pytest.fixture
def client():
    """TestClient para la aplicación orchestrator."""
    return TestClient(app)


@pytest.fixture
def use_case():
    """AsyncMock bound como la dependencia del router para las pruebas."""
    mock = AsyncMock()
    app.dependency_overrides[build_create_post_rf003_use_case] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


@pytest.fixture
def created_post_obj():
    """Objeto retornado por la ejecución exitosa del caso de uso RF003."""
    return CreatedPostResponse(
        id="PUB-555",
        user_id="USR-001",
        created_at=datetime(2026, 9, 3, 14, 0, 0, tzinfo=timezone.utc),
        expire_at=datetime(2026, 9, 10, 23, 59, 59, tzinfo=timezone.utc),
        route=CreatedRouteSummary(
            id="ROT-987",
            created_at=datetime(2026, 9, 3, 14, 0, 0, tzinfo=timezone.utc),
        ),
    )


@pytest.fixture
def valid_post_body():
    return {
        "flightId": "FL-12345",
        "expireAt": "2026-09-10T23:59:59Z",
        "plannedStartDate": "2026-09-12T08:00:00Z",
        "plannedEndDate": "2026-09-12T12:00:00Z",
        "origin": {
            "airportCode": "BOG",
            "country": "CO",
        },
        "destiny": {
            "airportCode": "MDE",
            "country": "CO",
        },
        "bagCost": 25.50,
    }


def test_create_publication_success_returns_201_envelope(
    client,
    use_case,
    created_post_obj,
    valid_post_body,
):
    """Una llamada exitosa a RF-003 retorna el envelope de respuesta con status 201."""
    use_case.execute.return_value = created_post_obj

    response = client.post("/rf003/posts", json=valid_post_body, headers=AUTH)

    assert response.status_code == 201
    body = response.json()
    assert body["data"]["id"] == created_post_obj.id
    assert body["data"]["userId"] == created_post_obj.user_id
    assert (
        datetime.fromisoformat(body["data"]["createdAt"]) == created_post_obj.created_at
    )
    assert body["msg"]


def test_missing_body_field_returns_400(client, valid_post_body):
    invalid_body = valid_post_body.copy()
    invalid_body.pop("flightId")
    response = client.post("/rf003/posts", json=invalid_body)
    assert response.status_code == 400


def test_invalid_body_types_returns_400(client, use_case, valid_post_body):
    """Un tipo de dato inválido (ej: costo de maleta no numérico) no pasa la validación."""
    response = client.post(
        "/rf003/posts",
        json={
            **valid_post_body,
            "bagCost": "not-a-number",
        },
        headers=AUTH,
    )

    assert response.status_code in (400, 422)
    use_case.execute.assert_not_awaited()


@pytest.mark.parametrize(
    ("error", "expected_status"),
    [
        (MissingTokenError(), 403),
        (InvalidTokenError(), 401),
        (InvalidDatesError(), 412),
        (InvalidExpirationDateError(), 412),
        (DuplicatePostError(), 412),
        (DownstreamUnavailableError(), 503),
    ],
)
def test_domain_errors_map_to_status_codes(
    client,
    use_case,
    valid_post_body,
    error,
    expected_status,
):
    """Cada excepción de dominio se mapea al código HTTP correspondiente con su mensaje."""
    use_case.execute.side_effect = error

    response = client.post("/rf003/posts", json=valid_post_body, headers=AUTH)

    assert response.status_code == expected_status
    assert "msg" in response.json()


def test_503_body_carries_the_spec_message(client, use_case, valid_post_body):
    """El payload de error 503 coincide con el mensaje requerido por la especificación."""
    use_case.execute.side_effect = DownstreamUnavailableError()

    response = client.post("/rf003/posts", json=valid_post_body, headers=AUTH)

    assert response.json()["msg"] == "El servicio está temporalmente fuera de servicio."


def test_token_is_forwarded_to_the_use_case(client, use_case, valid_post_body):
    """El token Bearer del encabezado de la petición se extrae y pasa al caso de uso."""
    use_case.execute.side_effect = MissingTokenError()

    client.post(
        "/rf003/posts",
        json=valid_post_body,
        headers={"Authorization": "Bearer abc123"},
    )

    assert use_case.execute.await_args.kwargs["token"] == "abc123"


def test_no_auth_header_passes_none_token(client, use_case, valid_post_body):
    """Sin encabezado Authorization, el caso de uso recibe token=None."""
    use_case.execute.side_effect = MissingTokenError()

    client.post("/rf003/posts", json=valid_post_body)

    assert use_case.execute.await_args.kwargs["token"] is None
