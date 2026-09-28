from abc import ABC, abstractmethod

from domain.models.post import Post
from entrypoints.api.schemas.post_filters import PostFilters


class PostRepositoryPort(ABC):
    """Post repository interface"""

    @abstractmethod
    def create(self, post: Post) -> Post:
        pass

    @abstractmethod
    def get_by_id(self, post_id: str) -> Post | None:
        """Get post by ID."""

    @abstractmethod
    def get_all(self, filters: PostFilters) -> list[Post]:
        """Get all posts."""

    @abstractmethod
    def delete(self, post_id: str) -> bool:
        """Delete a post."""

    @abstractmethod
    def count(self) -> int:
        """Return the number of posts."""

    @abstractmethod
    def reset(self) -> None:
        """Delete all posts."""
