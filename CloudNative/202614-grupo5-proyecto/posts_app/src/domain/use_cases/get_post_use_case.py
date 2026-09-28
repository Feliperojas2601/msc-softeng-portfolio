from domain.models.post import Post
from domain.ports.post_repository_port import PostRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import PostNotFoundError


class GetPostUseCase(BaseUseCase):
    """Use case for retrieving a post by its identifier."""

    def __init__(self, post_repository: PostRepositoryPort):
        self.post_repository = post_repository

    async def execute(self, post_id: str) -> Post | None:
        """Retrieve a post by its identifier."""
        post = await self.post_repository.get_by_id(post_id)
        if not post:
            raise PostNotFoundError()
        return post
