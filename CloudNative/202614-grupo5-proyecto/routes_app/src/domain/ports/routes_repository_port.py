from abc import ABC, abstractmethod

from domain.models.route import Route


class RoutesRepositoryPort(ABC):
    """Persistence operations required by the routes domain."""

    @abstractmethod
    async def create(self, route: Route) -> Route:
        """Persist a new route."""

    @abstractmethod
    async def get_by_flight_id(self, flight_id: str) -> list[Route]:
        """Return routes matching a flight identifier."""

    @abstractmethod
    async def get_all(self) -> list[Route]:
        """Return every stored route."""

    @abstractmethod
    async def get_by_id(self, route_id: str) -> Route | None:
        """Return a route by id or None when it does not exist."""

    @abstractmethod
    async def delete(self, route: Route) -> None:
        """Delete an existing route."""

    @abstractmethod
    async def count(self) -> int:
        """Count all stored routes."""

    @abstractmethod
    async def delete_all(self) -> None:
        """Delete every stored route."""


RoutesRepository = RoutesRepositoryPort
