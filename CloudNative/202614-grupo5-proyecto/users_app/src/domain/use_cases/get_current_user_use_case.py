from domain.models.user import User, UserStatus
from domain.ports.user_repository_port import UserRepositoryPort
from domain.services.token_service import is_expired
from domain.use_cases.base_use_case import BaseUseCase
from errors import InvalidTokenError


class GetCurrentUserUseCase(BaseUseCase):
    """Use case for resolving the user behind a session token."""

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    async def execute(self, token: str) -> User:
        """Return the user owning the given token, if it is still valid."""
        user = await self.user_repository.get_by_token(token)
        if not user or is_expired(user.expire_at):
            raise InvalidTokenError()
        if user.status != UserStatus.VERIFICADO:
            # A non-verified user's token must not grant access (RF-007); treated
            # the same as an invalid token since no dedicated status code is defined.
            raise InvalidTokenError()
        return user
