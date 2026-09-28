from abc import ABC, abstractmethod


class UsersPort(ABC):
    """Port for reading and updating a user's verification status in users_app."""

    @abstractmethod
    async def get_user(self, user_id: str) -> dict:
        """Fetch a user's public profile (id, email, fullName, status, etc.)."""

    @abstractmethod
    async def update_status(self, user_id: str, status: str) -> None:
        """Set a user's final verification status (VERIFICADO or NO_VERIFICADO)."""
