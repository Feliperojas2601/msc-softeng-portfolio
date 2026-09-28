from domain.ports.post_repository_port import PostRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import PostNotFoundError


class DeletePostUseCase(BaseUseCase):
    """Use case for deleting a post."""

    def __init__(self, post_repository: PostRepositoryPort):
        self.post_repository = post_repository

    async def execute(self, post_id: str) -> bool:
        """Delete a post by its identifier."""
        post = await self.post_repository.delete(post_id)
        if not post:
            raise PostNotFoundError()

        return post
