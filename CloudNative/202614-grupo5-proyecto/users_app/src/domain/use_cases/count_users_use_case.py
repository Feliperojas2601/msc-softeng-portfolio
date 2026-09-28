from domain.ports.user_repository_port import UserRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class CountUsersUseCase(BaseUseCase):
    """Use case for counting the total number of registered users."""

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    async def execute(self) -> int:
        """Return how many users exist."""
        return await self.user_repository.count()
