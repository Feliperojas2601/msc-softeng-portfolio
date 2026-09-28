import logging

from adapters.http.client import request
from domain.ports.notifications_port import NotificationsPort
from errors import DownstreamUnavailableError

logger = logging.getLogger(__name__)


class HttpNotificationsAdapter(NotificationsPort):
    """HTTP adapter for the notifications component.

    Contract (POST {base_url}/notify), to be confirmed with the team's
    notifications component:
    {
        "type": "IDENTITY_VERIFICATION",
        "userId": str,
        "email": str,
        "fullName": str | None,
        "status": "VERIFICADO" | "NO_VERIFICADO",
        "ruv": str,
    }

    A failure to notify does not fail the whole webhook: RF-007 requires the
    user to be notified regardless of the verification outcome, but the
    verification result itself (the user's status in users_app) has already
    been applied by the time this runs, so it must not be rolled back just
    because the notifications component is momentarily unreachable.
    """

    def __init__(self, base_url: str, timeout: float, max_retries: int):
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries

    async def notify_identity_result(
        self,
        user_id: str,
        email: str,
        full_name: str | None,
        status: str,
        ruv: str,
    ) -> None:
        """Best-effort notification of the identity verification result."""
        payload = {
            "type": "IDENTITY_VERIFICATION",
            "userId": user_id,
            "email": email,
            "fullName": full_name,
            "status": status,
            "ruv": ruv,
        }
        try:
            await request(
                "POST",
                f"{self._base_url}/notify",
                timeout=self._timeout,
                max_retries=self._max_retries,
                json=payload,
            )
        except DownstreamUnavailableError:
            logger.warning(
                "Failed to notify identity verification result for user %s", user_id
            )
