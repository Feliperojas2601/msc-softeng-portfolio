from domain.ports.routes_repository_port import RoutesRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class ResetRoutesUseCase(BaseUseCase):
    """Delete every route from the database."""

    def __init__(self, route_repository: RoutesRepositoryPort):
        self.route_repository = route_repository

    async def execute(self) -> None:
        """Delete all stored routes."""
        await self.route_repository.delete_all()
