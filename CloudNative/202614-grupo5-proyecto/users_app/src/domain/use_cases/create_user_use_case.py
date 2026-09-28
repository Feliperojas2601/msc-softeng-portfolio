import logging
import uuid

from domain.models.user import User, UserStatus
from domain.ports.identity_verification_port import IdentityVerificationPort
from domain.ports.user_repository_port import UserRepositoryPort
from domain.services.password_service import generate_salt, hash_password
from domain.services.token_service import utcnow
from domain.use_cases.base_use_case import BaseUseCase
from errors import IdentityVerificationRequestError, UserAlreadyExistsError

logger = logging.getLogger(__name__)


class CreateUserUseCase(BaseUseCase):
    """Use case for creating a new user."""

    def __init__(
        self,
        user_repository: UserRepositoryPort,
        identity_verification: IdentityVerificationPort,
        webhook_url: str,
    ):
        self.user_repository = user_repository
        self.identity_verification = identity_verification
        self.webhook_url = webhook_url

    async def execute(
        self,
        username: str,
        password: str,
        email: str,
        dni: str | None = None,
        full_name: str | None = None,
        phone_number: str | None = None,
    ) -> User:
        """Create a new user, failing if the username or email are already taken."""
        if await self.user_repository.get_by_username(username):
            raise UserAlreadyExistsError()
        if await self.user_repository.get_by_email(email):
            raise UserAlreadyExistsError()

        salt = generate_salt()
        now = utcnow()
        user = User(
            id=str(uuid.uuid4()),
            username=username,
            email=email,
            dni=dni,
            full_name=full_name,
            phone_number=phone_number,
            password=hash_password(password, salt),
            salt=salt,
            token=None,
            status=UserStatus.POR_VERIFICAR,
            expire_at=None,
            created_at=now,
            updated_at=now,
        )
        created_user = await self.user_repository.create(user)

        try:
            await self.identity_verification.request_verification(
                user_id=created_user.id,
                transaction_identifier=str(uuid.uuid4()),
                webhook_url=self.webhook_url,
                email=created_user.email,
                dni=created_user.dni,
                full_name=created_user.full_name,
                phone_number=created_user.phone_number,
            )
        except IdentityVerificationRequestError:
            # The user stays POR_VERIFICAR; a retry mechanism is out of scope for
            # this use case and left for future work. Creation itself must not fail
            # just because the external provider is momentarily unreachable.
            logger.warning(
                "Failed to request identity verification for user %s",
                created_user.id,
            )

        return created_user
