from domain.models.user import User
from domain.ports.user_repository_port import UserRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import UserNotFoundError


class GetUserByIdUseCase(BaseUseCase):
    """Use case for fetching a user's public data by its id."""

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    async def execute(self, user_id: str) -> User:
        """Return the user matching the given id, raising if it does not exist."""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user
