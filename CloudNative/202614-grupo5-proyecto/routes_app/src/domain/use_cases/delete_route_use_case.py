from domain.ports.routes_repository_port import RoutesRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import RouteNotFoundError


class DeleteRouteUseCase(BaseUseCase):
    """Delete a route by its identifier."""

    def __init__(self, route_repository: RoutesRepositoryPort):
        self.route_repository = route_repository

    async def execute(self, route_id: str) -> None:
        """Delete a route or fail when it does not exist."""
        route = await self.route_repository.get_by_id(route_id)
        if route is None:
            raise RouteNotFoundError()
        await self.route_repository.delete(route)
