from datetime import UTC, datetime
from uuid import uuid4

from domain.models.post import Post
from domain.ports.post_repository_port import PostRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from entrypoints.api.schemas.create_post import CreatePost
from errors import ExpirationDateNoValid


class CreatePostUseCase(BaseUseCase):
    """Use case for saving a post"""

    def __init__(self, post_repository: PostRepositoryPort):
        self.post_repository = post_repository

    async def execute(self, data: CreatePost) -> CreatePost:
        """Create a new post."""

        if data.expireAt <= datetime.now(UTC):
            raise ExpirationDateNoValid()

        post = Post(
            id=str(uuid4()),
            routeId=str(data.routeId),
            userId=str(data.userId),
            expireAt=data.expireAt,
            createdAt=datetime.now(UTC),
        )

        return await self.post_repository.create(post)
