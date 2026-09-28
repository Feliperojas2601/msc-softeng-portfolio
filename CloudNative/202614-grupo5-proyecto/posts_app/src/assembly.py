from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.database.postgres_post_repository import SQLAlchemyPostRepositoryAdapter
from adapters.database.session import get_session
from domain.use_cases.count_posts_use_case import CountPostsUseCase
from domain.use_cases.create_post_use_case import CreatePostUseCase
from domain.use_cases.delete_post_use_case import DeletePostUseCase
from domain.use_cases.get_post_filter_use_case import GetPostFiltersUseCase
from domain.use_cases.get_post_use_case import GetPostUseCase
from domain.use_cases.reset_posts_use_case import ResetPostsUseCase


def build_post_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLAlchemyPostRepositoryAdapter:
    """Build the post repository adapter bound to a request-scoped session."""
    return SQLAlchemyPostRepositoryAdapter(session)


def build_create_post_use_case(
    repository: SQLAlchemyPostRepositoryAdapter = Depends(build_post_repository),
) -> CreatePostUseCase:
    """Build the create post use case."""
    return CreatePostUseCase(repository)


def build_get_post_filter_use_case(
    repository: SQLAlchemyPostRepositoryAdapter = Depends(build_post_repository),
) -> GetPostFiltersUseCase:
    """Build the get post by ID use case."""
    return GetPostFiltersUseCase(repository)


def build_get_post_by_id_use_case(
    repository: SQLAlchemyPostRepositoryAdapter = Depends(build_post_repository),
) -> GetPostUseCase:
    """Build the get all posts use case."""
    return GetPostUseCase(repository)


def build_delete_post_use_case(
    repository: SQLAlchemyPostRepositoryAdapter = Depends(build_post_repository),
) -> DeletePostUseCase:
    """Build the delete post use case."""
    return DeletePostUseCase(repository)


def build_count_posts_use_case(
    repository: SQLAlchemyPostRepositoryAdapter = Depends(build_post_repository),
) -> CountPostsUseCase:
    """Build the count posts use case."""
    return CountPostsUseCase(repository)


def build_reset_posts_use_case(
    repository: SQLAlchemyPostRepositoryAdapter = Depends(build_post_repository),
) -> ResetPostsUseCase:
    """Build the reset posts use case."""
    return ResetPostsUseCase(repository)
