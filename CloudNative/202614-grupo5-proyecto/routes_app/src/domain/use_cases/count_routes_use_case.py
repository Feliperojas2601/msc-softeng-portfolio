from domain.ports.routes_repository_port import RoutesRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class CountRoutesUseCase(BaseUseCase):
    """Count the routes stored in the database."""

    def __init__(self, route_repository: RoutesRepositoryPort):
        self.route_repository = route_repository

    async def execute(self) -> int:
        """Return the number of routes."""
        return await self.route_repository.count()
