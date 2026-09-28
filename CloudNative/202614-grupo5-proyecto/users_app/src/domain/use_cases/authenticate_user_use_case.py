from domain.models.user import User, UserStatus
from domain.ports.user_repository_port import UserRepositoryPort
from domain.services.password_service import verify_password
from domain.services.token_service import compute_expiration, generate_token, utcnow
from domain.use_cases.base_use_case import BaseUseCase
from errors import InvalidCredentialsError, UserNotVerifiedError


class AuthenticateUserUseCase(BaseUseCase):
    """Use case for generating a new session token for a user."""

    def __init__(
        self, user_repository: UserRepositoryPort, token_expiration_hours: int
    ):
        self.user_repository = user_repository
        self.token_expiration_hours = token_expiration_hours

    async def execute(self, username: str, password: str) -> User:
        """Validate credentials and issue a new session token."""
        user = await self.user_repository.get_by_username(username)
        if not user or not verify_password(password, user.salt, user.password):
            raise InvalidCredentialsError()
        if user.status != UserStatus.VERIFICADO:
            raise UserNotVerifiedError()

        user.token = generate_token()
        user.expire_at = compute_expiration(self.token_expiration_hours)
        user.updated_at = utcnow()

        return await self.user_repository.update(user)
