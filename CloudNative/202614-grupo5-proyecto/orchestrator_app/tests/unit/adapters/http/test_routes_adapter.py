import json
from datetime import UTC, datetime

import httpx
import pytest
import respx

from adapters.http.routes_adapter import HttpRoutesAdapter
from errors import DownstreamUnavailableError

BASE = "http://routes.test"


@pytest.fixture
def adapter() -> HttpRoutesAdapter:
    """Un adaptador de rutas configurado con reintento."""
    return HttpRoutesAdapter(BASE, timeout=1.0, max_retries=1)


@respx.mock
async def test_get_route_projects_bag_cost(adapter: HttpRoutesAdapter):
    """Una respuesta 200 proyecta la respuesta en un Route con el costo de equipaje."""
    respx.get(f"{BASE}/routes/route-1").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "route-1",
                "flightId": "AV123",
                "bagCost": 25,
                "sourceCountry": "CO",
            },
        )
    )

    route = await adapter.get_route("route-1")

    assert route.id == "route-1"
    assert route.bag_cost == 25.0


@respx.mock
@pytest.mark.parametrize("status_code", [404, 500, 503])
async def test_get_route_maps_any_non_200_to_downstream_unavailable(
    adapter: HttpRoutesAdapter, status_code: int
):
    """Cualquier código distinto a 200 lanza DownstreamUnavailableError."""
    respx.get(f"{BASE}/routes/route-1").mock(return_value=httpx.Response(status_code))

    with pytest.raises(DownstreamUnavailableError):
        await adapter.get_route("route-1")


@respx.mock
async def test_get_route_retries_once_on_transport_error(adapter: HttpRoutesAdapter):
    """Un error transitorio de conexión se reintenta y luego puede ser exitoso."""
    route = respx.get(f"{BASE}/routes/route-1")
    route.side_effect = [
        httpx.ConnectError("boom"),
        httpx.Response(200, json={"id": "route-1", "bagCost": 10}),
    ]

    result = await adapter.get_route("route-1")

    assert result.bag_cost == 10.0
    assert route.call_count == 2


@respx.mock
async def test_get_route_detail_projects_all_fields(adapter: HttpRoutesAdapter):
    """Un response 200 se proyecta en un RouteDetail con todos los campos."""
    respx.get(f"{BASE}/routes/route-1").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "route-1",
                "flightId": "AV123",
                "sourceAirportCode": "BOG",
                "sourceCountry": "Colombia",
                "destinyAirportCode": "MIA",
                "destinyCountry": "Estados Unidos",
                "bagCost": 20.0,
                "plannedStartDate": "2026-06-10T08:00:00Z",
                "plannedEndDate": "2026-06-10T12:00:00Z",
                "createdAt": "2026-01-01T00:00:00Z",
            },
        )
    )

    route = await adapter.get_route_detail("route-1")

    assert route.id == "route-1"
    assert route.flight_id == "AV123"
    assert route.destiny_airport_code == "MIA"
    assert route.bag_cost == 20.0
    assert route.planned_start_date is not None


@respx.mock
@pytest.mark.parametrize("status_code", [404, 500, 503])
async def test_get_route_detail_maps_any_non_200_to_downstream_unavailable(
    adapter: HttpRoutesAdapter, status_code: int
):
    """Cualquier código de estado distinto a 200 lanza DownstreamUnavailableError."""
    respx.get(f"{BASE}/routes/route-1").mock(return_value=httpx.Response(status_code))

    with pytest.raises(DownstreamUnavailableError):
        await adapter.get_route_detail("route-1")


@respx.mock
async def test_get_routes_success_with_filters(adapter: HttpRoutesAdapter):
    """GET /routes con parámetro de consulta 'flight' retorna lista de RouteDetail."""
    route = respx.get(f"{BASE}/routes").mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "id": "route-1",
                    "flightId": "AV123",
                    "sourceAirportCode": "BOG",
                    "sourceCountry": "CO",
                    "destinyAirportCode": "MIA",
                    "destinyCountry": "US",
                    "bagCost": 50.0,
                    "createdAt": "2026-01-01T00:00:00Z",
                }
            ],
        )
    )

    routes = await adapter.get_routes(flight_id="AV123")

    assert route.called
    assert route.calls.last.request.url.query.decode() == "flight=AV123"
    assert len(routes) == 1
    assert routes[0].id == "route-1"
    assert routes[0].flight_id == "AV123"


@respx.mock
async def test_get_routes_error_raises_downstream_unavailable(
    adapter: HttpRoutesAdapter,
):
    """Si GET /routes no retorna 200, eleva DownstreamUnavailableError."""
    respx.get(f"{BASE}/routes").mock(return_value=httpx.Response(500))

    with pytest.raises(DownstreamUnavailableError):
        await adapter.get_routes()


@respx.mock
async def test_create_route_success(adapter: HttpRoutesAdapter):
    """POST /routes envía los datos correctamente y retorna un CreatedRoute."""
    start_date = datetime(2026, 6, 1, 10, 0, 0, tzinfo=UTC)
    end_date = datetime(2026, 6, 1, 14, 0, 0, tzinfo=UTC)

    route = respx.post(f"{BASE}/routes").mock(
        return_value=httpx.Response(
            201,
            json={
                "id": "route-99",
                "createdAt": "2026-01-01T10:00:00Z",
            },
        )
    )

    result = await adapter.create_route(
        flight_id="LA800",
        source_airport_code="SCL",
        source_country="CL",
        destiny_airport_code="BOG",
        destiny_country="CO",
        bag_cost=30.0,
        planned_start_date=start_date,
        planned_end_date=end_date,
    )

    assert route.called
    payload = json.loads(route.calls.last.request.content)
    assert payload["flightId"] == "LA800"
    assert payload["sourceAirportCode"] == "SCL"
    assert payload["bagCost"] == 30.0
    assert "2026-06-01T10:00:00" in payload["plannedStartDate"]

    assert result.id == "route-99"


@respx.mock
async def test_create_route_error_raises_downstream_unavailable(
    adapter: HttpRoutesAdapter,
):
    """POST /routes con código != 200/201 lanza DownstreamUnavailableError."""
    respx.post(f"{BASE}/routes").mock(return_value=httpx.Response(400))

    with pytest.raises(DownstreamUnavailableError):
        await adapter.create_route(
            flight_id="LA800",
            source_airport_code="SCL",
            source_country="CL",
            destiny_airport_code="BOG",
            destiny_country="CO",
            bag_cost=30.0,
        )


@respx.mock
@pytest.mark.parametrize("status_code", [200, 204, 404])
async def test_delete_route_allowed_status_codes(
    adapter: HttpRoutesAdapter, status_code: int
):
    """DELETE /routes/{id} finaliza con éxito en respuestas 200, 204 o 404."""
    route = respx.delete(f"{BASE}/routes/route-1").mock(
        return_value=httpx.Response(status_code)
    )

    await adapter.delete_route("route-1")
    assert route.called


@respx.mock
async def test_delete_route_error_raises_downstream_unavailable(
    adapter: HttpRoutesAdapter,
):
    """DELETE /routes/{id} con respuesta 500 lanza DownstreamUnavailableError."""
    respx.delete(f"{BASE}/routes/route-1").mock(return_value=httpx.Response(500))

    with pytest.raises(DownstreamUnavailableError):
        await adapter.delete_route("route-1")
