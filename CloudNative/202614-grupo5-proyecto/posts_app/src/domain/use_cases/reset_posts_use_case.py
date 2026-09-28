from domain.ports.post_repository_port import PostRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class ResetPostsUseCase(BaseUseCase):
    """Use case for resetting the posts database."""

    def __init__(self, post_repository: PostRepositoryPort):
        self.post_repository = post_repository

    async def execute(self) -> None:
        """Delete all posts."""
        await self.post_repository.reset()
