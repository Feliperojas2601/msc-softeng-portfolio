from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from assembly import (
    build_count_routes_use_case,
    build_create_route_use_case,
    build_delete_route_use_case,
    build_get_route_use_case,
    build_get_routes_use_case,
    build_reset_routes_use_case,
)
from entrypoints.api.main import app
from entrypoints.api.schemas.route_schemas import CreateRouteRequest, RouteResponse
from errors import InvalidRouteDatesError, RouteAlreadyExistsError, RouteNotFoundError
from tests.unit.conftest import ROUTE_ID

client = TestClient(app)


def override(dependency, result=None, side_effect=None) -> AsyncMock:
    """Replace one assembled use case with an async mock."""
    execute = AsyncMock(return_value=result, side_effect=side_effect)
    fake = SimpleNamespace(execute=execute)
    app.dependency_overrides[dependency] = lambda: fake
    return execute


@pytest.fixture(autouse=True)
def clear_overrides():
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


def test_create_route_returns_contract(route_data, existing_route):
    execute = override(build_create_route_use_case, existing_route)
    response = client.post("/routes", json=route_data)

    assert response.status_code == 201
    assert response.json() == {
        "id": ROUTE_ID,
        "createdAt": "2026-01-01T12:00:00",
    }
    assert execute.await_args.kwargs["flight_id"] == "FL-001"


def test_create_route_validates_body(route_data):
    override(build_create_route_use_case)
    route_data.pop("flightId")
    assert client.post("/routes", json=route_data).status_code == 400


def test_create_route_rejects_invalid_airport(route_data):
    override(build_create_route_use_case)
    route_data["sourceAirportCode"] = "INVALID"
    assert client.post("/routes", json=route_data).status_code == 400


def test_create_route_maps_business_errors(route_data):
    override(build_create_route_use_case, side_effect=RouteAlreadyExistsError())
    duplicate = client.post("/routes", json=route_data)
    assert duplicate.status_code == 412
    assert duplicate.json() == {}

    override(build_create_route_use_case, side_effect=InvalidRouteDatesError())
    invalid_dates = client.post("/routes", json=route_data)
    assert invalid_dates.status_code == 412
    assert invalid_dates.json() == {"msg": "Las fechas del trayecto no son válidas"}


def test_list_routes_and_filter(existing_route):
    execute = override(build_get_routes_use_case, [existing_route])
    response = client.get("/routes")
    assert response.status_code == 200
    assert response.json()[0] == {
        "id": ROUTE_ID,
        "flightId": "FL-001",
        "sourceAirportCode": "BOG",
        "sourceCountry": "Colombia",
        "destinyAirportCode": "MEX",
        "destinyCountry": "México",
        "bagCost": 120,
        "plannedStartDate": "2099-01-01T10:00:00",
        "plannedEndDate": "2099-01-01T14:00:00",
        "createdAt": "2026-01-01T12:00:00",
        "updatedAt": "2026-01-01T12:00:00",
    }
    execute.assert_awaited_once_with(None)

    response = client.get("/routes?flight=FL-001")
    assert response.status_code == 200
    execute.assert_awaited_with("FL-001")


def test_list_routes_rejects_empty_filter():
    override(build_get_routes_use_case, [])
    assert client.get("/routes?flight=").status_code == 400


def test_get_route_success_invalid_id_and_not_found(existing_route):
    override(build_get_route_use_case, existing_route)
    response = client.get(f"/routes/{ROUTE_ID}")
    assert response.status_code == 200
    assert response.json()["id"] == ROUTE_ID

    assert client.get("/routes/not-a-uuid").status_code == 400

    override(build_get_route_use_case, side_effect=RouteNotFoundError())
    assert client.get(f"/routes/{ROUTE_ID}").status_code == 404


def test_delete_route_success_invalid_id_and_not_found():
    execute = override(build_delete_route_use_case)
    response = client.delete(f"/routes/{ROUTE_ID}")
    assert response.status_code == 200
    assert response.json() == {"msg": "el trayecto fue eliminado"}
    execute.assert_awaited_once_with(ROUTE_ID)

    assert client.delete("/routes/not-a-uuid").status_code == 400

    override(build_delete_route_use_case, side_effect=RouteNotFoundError())
    assert client.delete(f"/routes/{ROUTE_ID}").status_code == 404


def test_count_ping_and_reset():
    override(build_count_routes_use_case, 4)
    assert client.get("/routes/count").json() == {"count": 4}

    ping = client.get("/routes/ping")
    assert ping.status_code == 200
    assert ping.text == "pong"

    execute = override(build_reset_routes_use_case)
    reset = client.post("/routes/reset")
    assert reset.status_code == 200
    assert reset.json() == {"msg": "Todos los datos fueron eliminados"}
    execute.assert_awaited_once()


def test_openapi_contains_all_route_operations():
    document = app.openapi()
    assert "/routes" in document["paths"]
    assert "/routes/count" in document["paths"]
    assert "/routes/ping" in document["paths"]
    assert "/routes/reset" in document["paths"]
    assert "/routes/{route_id}" in document["paths"]


def test_openapi_describes_the_complete_route_entity():
    document = app.openapi()
    schemas = document["components"]["schemas"]
    schema = schemas["RouteResponse"]
    properties = schema["properties"]
    request_properties = schemas["CreateRouteRequest"]["properties"]

    expected_fields = {
        "id",
        "flightId",
        "sourceAirportCode",
        "sourceCountry",
        "destinyAirportCode",
        "destinyCountry",
        "bagCost",
        "plannedStartDate",
        "plannedEndDate",
        "createdAt",
        "updatedAt",
    }
    assert set(properties) == expected_fields
    assert set(schema["required"]) == expected_fields
    assert properties["id"]["type"] == "string"
    assert properties["flightId"]["type"] == "string"
    assert schemas["AirportCode"]["type"] == "string"
    assert properties["bagCost"]["type"] == "integer"
    for field in ("plannedStartDate", "plannedEndDate", "createdAt", "updatedAt"):
        assert properties[field]["type"] == "string"
        assert properties[field]["format"] == "date-time"
    assert set(request_properties) == expected_fields - {"id", "createdAt", "updatedAt"}
    assert all(
        field.alias is None for field in CreateRouteRequest.model_fields.values()
    )
    assert all(field.alias is None for field in RouteResponse.model_fields.values())
    assert "example" not in schema
    assert all("examples" not in value for value in properties.values())
