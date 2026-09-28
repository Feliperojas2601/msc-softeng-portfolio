from domain.models.user import User, UserStatus
from domain.ports.user_repository_port import UserRepositoryPort
from domain.services.token_service import utcnow
from domain.use_cases.base_use_case import BaseUseCase
from errors import UserNotFoundError


class UpdateUserUseCase(BaseUseCase):
    """Use case for updating an existing user's profile fields."""

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    async def execute(
        self,
        user_id: str,
        status: UserStatus | None = None,
        dni: str | None = None,
        full_name: str | None = None,
        phone_number: str | None = None,
    ) -> User:
        """Update only the provided fields of an existing user."""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        if status is not None:
            user.status = status
        if dni is not None:
            user.dni = dni
        if full_name is not None:
            user.full_name = full_name
        if phone_number is not None:
            user.phone_number = phone_number
        user.updated_at = utcnow()

        return await self.user_repository.update(user)
