from domain.models.post import Post
from domain.ports.post_repository_port import PostRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from entrypoints.api.schemas.post_filters import PostFilters


class GetPostFiltersUseCase(BaseUseCase):
    """Use case for searching posts."""

    def __init__(self, post_repository: PostRepositoryPort):
        self.post_repository = post_repository

    async def execute(self, filters: PostFilters) -> list[Post]:
        """Return posts matching the provided filters."""
        return await self.post_repository.get_all(filters)
