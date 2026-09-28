from domain.models.route import Route
from domain.ports.routes_repository_port import RoutesRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class GetRoutesUseCase(BaseUseCase):
    """List all routes or filter them by flight id."""

    def __init__(self, route_repository: RoutesRepositoryPort):
        self.route_repository = route_repository

    async def execute(self, flight_id: str | None = None) -> list[Route]:
        """Return routes matching the optional filter."""
        if flight_id is not None:
            return await self.route_repository.get_by_flight_id(flight_id)
        return await self.route_repository.get_all()
