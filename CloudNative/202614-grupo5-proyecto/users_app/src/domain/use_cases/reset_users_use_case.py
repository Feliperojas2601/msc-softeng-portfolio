from domain.ports.user_repository_port import UserRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class ResetUsersUseCase(BaseUseCase):
    """Use case for wiping every user, used to reset the database."""

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    async def execute(self) -> None:
        """Delete every stored user."""
        await self.user_repository.delete_all()
