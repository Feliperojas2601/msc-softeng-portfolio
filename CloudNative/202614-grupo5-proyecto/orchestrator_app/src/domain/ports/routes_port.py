from abc import ABC, abstractmethod
from datetime import datetime

from domain.models.route import CreatedRoute, Route, RouteDetail


class RoutesPort(ABC):
    """Interfaz para interactuar con el servicio de rutas."""

    @abstractmethod
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
    ) -> CreatedRoute:
        """Crea una nueva ruta en el servicio externo de rutas.

        Args:
            flight_id: Identificador del vuelo.
            source_airport_code: Código del aeropuerto de origen.
            source_country: Nombre del país de origen.
            destiny_airport_code: Código del aeropuerto de destino.
            destiny_country: Nombre del país de destino.
            bag_cost: Costo de envío de maleta.
            planned_start_date: Fecha planeada de inicio (opcional).
            planned_end_date: Fecha planeada de finalización (opcional).

        Returns:
            RouteDetail: La ruta recién creada devuelta por el servicio.

        Raises:
            DownstreamUnavailableError: El servicio de rutas no pudo ser alcanzado.
        """

    @abstractmethod
    async def get_route(self, route_id: str) -> Route:
        """Obtiene una ruta por identificador.

        Args:
            route_id: Identificador de la ruta a obtener.

        Returns:
            Route: La ruta obtenida, con su identificador y costo de envío de maleta.

        Raises:
            DownstreamUnavailableError: El servicio de rutas no pudo ser alcanzado.
        """

    @abstractmethod
    async def get_routes(self, flight_id: str) -> list[RouteDetail]:
        """Obtiene una lista de rutas, opcionalmente filtradas por identificador de vuelo.

        Args:
            flight_id: Identificador opcional del vuelo para filtrar las rutas.

        Returns:
            list[Route]: Lista de rutas encontradas.

        Raises:
            DownstreamUnavailableError: El servicio de rutas no pudo ser alcanzado.
        """

    @abstractmethod
    async def get_route_detail(self, route_id: str) -> RouteDetail:
        """Obtiene el detalle completo de un trayecto.

        Args:
            route_id: Identificador del trayecto a obtener.

        Returns:
            RouteDetail: El trayecto completo, incluidas las fechas planeadas.

        Raises:
            DownstreamUnavailableError: El servicio de rutas no pudo ser alcanzado.
        """

    @abstractmethod
    async def delete_route(self, route_id: str) -> None:
        """Elimina una ruta por su identificador en el servicio downstream.

        Acción compensatoria utilizada por la Saga cuando falla la creación del Post.

        Args:
            route_id: Identificador único de la ruta a eliminar.

        Raises:
            DownstreamUnavailableError: El servicio de rutas no respondió adecuadamente.
        """
