from abc import ABC, abstractmethod


class NotificationsPort(ABC):
    """Port for notifying the outcome of an identity verification."""

    @abstractmethod
    async def notify_identity_result(
        self,
        user_id: str,
        email: str,
        full_name: str | None,
        status: str,
        ruv: str,
    ) -> None:
        """Notify the result of an identity verification, regardless of outcome."""
