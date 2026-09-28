from domain.ports.notifications_port import NotificationsPort
from domain.ports.users_port import UsersPort
from errors import InvalidSignatureError
from signature import is_signature_valid


class ProcessVerificationCallbackUseCase:
    """Use case for validating and applying a TrueNative identity verification callback."""

    def __init__(
        self, users: UsersPort, notifications: NotificationsPort, secret_token: str
    ):
        self.users = users
        self.notifications = notifications
        self.secret_token = secret_token

    async def execute(
        self, ruv: str, user_id: str, status: str, score: float, verify_token: str
    ) -> None:
        """Validate the callback and, if trusted, update the user and notify the result.

        Updates the user's final status in users_app and notifies the result
        (regardless of outcome), per RF-007's acceptance criteria.

        Args:
            ruv: TrueNative's unique verification record identifier.
            user_id: The id of the user this verification is for.
            status: Final status reported by TrueNative (VERIFICADO or
                NO_VERIFICADO).
            score: Confidence score (0-100) reported by TrueNative.
            verify_token: Signature to validate the callback's authenticity.

        Raises:
            InvalidSignatureError: verify_token does not match the expected
                signature, so the callback is not trusted.
        """
        VERIFICATION_THRESHOLD = 60
        
        if not is_signature_valid(self.secret_token, ruv, score, verify_token):
            raise InvalidSignatureError(f"Invalid verifyToken for RUV {ruv}")

        final_status = "VERIFICADO" if score >= VERIFICATION_THRESHOLD else "NO_VERIFICADO"

        user = await self.users.get_user(user_id)
        await self.users.update_status(user_id, final_status)
        await self.notifications.notify_identity_result(
            user_id=user_id,
            email=user["email"],
            full_name=user.get("fullName"),
            status=status,
            ruv=ruv,
        )
