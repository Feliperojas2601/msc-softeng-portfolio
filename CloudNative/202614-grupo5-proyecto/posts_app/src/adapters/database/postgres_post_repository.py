from datetime import UTC, datetime

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.database.mappers import post_entity_to_model, post_model_to_entity
from adapters.database.post_model import PostModel
from domain.models.post import Post
from domain.ports.post_repository_port import PostRepositoryPort
from entrypoints.api.schemas.post_filters import PostFilters


class SQLAlchemyPostRepositoryAdapter(PostRepositoryPort):
    """PostgreSQL implementation of PostRepositoryPort using SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, post: Post) -> Post:
        """Persist a new post."""
        post_model = post_entity_to_model(post)
        self.session.add(post_model)
        await self.session.commit()
        await self.session.refresh(post_model)
        return post_model_to_entity(post_model)

    async def get_by_id(self, post_id: str) -> Post | None:
        """Get post by ID."""
        result = await self.session.execute(
            select(PostModel).where(PostModel.id == post_id)
        )
        post_model = result.scalar_one_or_none()
        return post_model_to_entity(post_model) if post_model else None

    async def get_all(self, filters: PostFilters) -> list[Post]:
        """Get all posts matching the given filters."""
        query = select(PostModel)

        if filters.route is not None:
            query = query.where(PostModel.route_id == filters.route)

        if filters.owner is not None:
            query = query.where(PostModel.user_id == filters.owner)

        if filters.expire is not None:
            now = datetime.now(UTC)
            if filters.expire:
                query = query.where(PostModel.expire_at <= now)
            else:
                query = query.where(PostModel.expire_at > now)

        result = await self.session.execute(query)
        post_models = result.scalars().all()
        return [post_model_to_entity(model) for model in post_models]

    async def delete(self, post_id: str) -> bool:
        """Delete a post by ID."""
        result = await self.session.execute(
            delete(PostModel).where(PostModel.id == post_id)
        )
        await self.session.commit()
        return result.rowcount > 0

    async def count(self) -> int:
        """Return the total number of posts."""
        result = await self.session.execute(select(func.count()).select_from(PostModel))
        return result.scalar_one()

    async def reset(self) -> None:
        """Delete all posts."""
        await self.session.execute(delete(PostModel))
        await self.session.commit()
