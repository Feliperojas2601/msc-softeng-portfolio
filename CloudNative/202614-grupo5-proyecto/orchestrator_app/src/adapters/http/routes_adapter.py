from datetime import datetime
from typing import Any

from adapters.http.client import request
from domain.models.route import CreatedRoute, Route, RouteDetail
from domain.ports.routes_port import RoutesPort
from errors import DownstreamUnavailableError


class HttpRoutesAdapter(RoutesPort):
    """Servicio adaptador HTTP para la obtención de rutas."""

    def __init__(self, base_url: str, timeout: float, max_retries: int):
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries

    async def get_route(self, route_id: str) -> Route:
        """Obtiene una ruta por identificador."""
        try:
            response = await request(
                "GET",
                f"{self._base_url}/routes/{route_id}",
                timeout=self._timeout,
                max_retries=self._max_retries,
            )
        except Exception as exc:
            raise DownstreamUnavailableError() from exc

        if response.status_code != 200:
            raise DownstreamUnavailableError()

        body = response.json()
        return Route(id=body["id"], bag_cost=body["bagCost"])

    async def get_route_detail(self, route_id: str) -> RouteDetail:
        """Obtiene el detalle completo de un trayecto."""
        try:
            response = await request(
                "GET",
                f"{self._base_url}/routes/{route_id}",
                timeout=self._timeout,
                max_retries=self._max_retries,
            )
        except Exception as exc:
            raise DownstreamUnavailableError() from exc

        if response.status_code != 200:
            raise DownstreamUnavailableError()

        return RouteDetail.model_validate(response.json())

    async def get_routes(self, flight_id: str | None = None) -> list[RouteDetail]:
        """Obtiene la lista de rutas, opcionalmente filtrada por flight_id."""
        params: dict[str, Any] = {}
        if flight_id:
            params["flight"] = flight_id

        try:
            response = await request(
                "GET",
                f"{self._base_url}/routes",
                params=params,
                timeout=self._timeout,
                max_retries=self._max_retries,
            )
        except Exception as exc:
            raise DownstreamUnavailableError() from exc

        if response.status_code != 200:
            raise DownstreamUnavailableError()

        body = response.json()
        return [RouteDetail.model_validate(item) for item in body]

    async def create_route(
        self,
        flight_id: str,
        source_airport_code: str,
        source_country: str,
        destiny_airport_code: str,
        destiny_country: str,
        bag_cost: float,
        planned_start_date: datetime | None = None,
        planned_end_date: datetime | None = None,
    ) -> RouteDetail:
        """Crea una nueva ruta enviando los datos al servicio externo mediante POST /routes."""
        payload: dict[str, Any] = {
            "flightId": flight_id,
            "sourceAirportCode": source_airport_code,
            "sourceCountry": source_country,
            "destinyAirportCode": destiny_airport_code,
            "destinyCountry": destiny_country,
            "bagCost": bag_cost,
        }

        if planned_start_date:
            payload["plannedStartDate"] = planned_start_date.isoformat()
        if planned_end_date:
            payload["plannedEndDate"] = planned_end_date.isoformat()

        try:
            response = await request(
                "POST",
                f"{self._base_url}/routes",
                json=payload,
                timeout=self._timeout,
                max_retries=self._max_retries,
            )
        except Exception as exc:
            raise DownstreamUnavailableError() from exc

        if response.status_code not in (200, 201, 404):
            raise DownstreamUnavailableError()

        return CreatedRoute.model_validate(response.json())

    async def delete_route(self, route_id: str) -> None:
        route_id_str = str(route_id)
        print(f"[COMPENSACION] Intentando DELETE /routes/{route_id_str}", flush=True)
        try:
            response = await request(
                "DELETE",
                f"{self._base_url}/routes/{route_id_str}",
                timeout=self._timeout,
                max_retries=self._max_retries,
            )
        except Exception as exc:
            print(f"[COMPENSACION] EXCEPCION: {exc}", flush=True)
            raise DownstreamUnavailableError() from exc

        print(
            f"[COMPENSACION] Status: {response.status_code} Body: {response.text}",
            flush=True,
        )

        if response.status_code not in (200, 204, 404):
            raise DownstreamUnavailableError()
