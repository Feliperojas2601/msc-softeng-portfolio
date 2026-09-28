from abc import ABC, abstractmethod

from domain.models.user import User


class UserRepositoryPort(ABC):
    """User repository interface."""

    @abstractmethod
    async def create(self, user: User) -> User:
        """Persist a new user."""

    @abstractmethod
    async def get_by_id(self, user_id: str) -> User | None:
        """Fetch a user by its id."""

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        """Fetch a user by its username."""

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """Fetch a user by its email."""

    @abstractmethod
    async def get_by_token(self, token: str) -> User | None:
        """Fetch a user by its current session token."""

    @abstractmethod
    async def update(self, user: User) -> User:
        """Persist changes made to an existing user."""

    @abstractmethod
    async def count(self) -> int:
        """Count how many users exist."""

    @abstractmethod
    async def delete_all(self) -> None:
        """Delete every user, used to reset the database."""
