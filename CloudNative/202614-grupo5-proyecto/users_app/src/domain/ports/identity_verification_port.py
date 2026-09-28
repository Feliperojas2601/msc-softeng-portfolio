from abc import ABC, abstractmethod


class IdentityVerificationPort(ABC):
    """Port for requesting user identity verification from an external provider."""

    @abstractmethod
    async def request_verification(
        self,
        user_id: str,
        transaction_identifier: str,
        webhook_url: str,
        email: str,
        dni: str | None = None,
        full_name: str | None = None,
        phone_number: str | None = None,
    ) -> None:
        """Request identity verification for a user; the result arrives later via webhook."""
