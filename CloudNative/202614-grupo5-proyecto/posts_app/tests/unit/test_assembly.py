from unittest.mock import MagicMock

from adapters.database.postgres_post_repository import SQLAlchemyPostRepositoryAdapter
from assembly import (
    build_count_posts_use_case,
    build_create_post_use_case,
    build_delete_post_use_case,
    build_get_post_by_id_use_case,
    build_get_post_filter_use_case,
    build_post_repository,
    build_reset_posts_use_case,
)
from domain.use_cases.count_posts_use_case import CountPostsUseCase
from domain.use_cases.create_post_use_case import CreatePostUseCase
from domain.use_cases.delete_post_use_case import DeletePostUseCase
from domain.use_cases.get_post_filter_use_case import GetPostFiltersUseCase
from domain.use_cases.get_post_use_case import GetPostUseCase
from domain.use_cases.reset_posts_use_case import ResetPostsUseCase


def test_build_post_repository_wraps_the_given_session():
    """build_post_repository binds the injected session to the adapter."""
    session = MagicMock()

    repository = build_post_repository(session)

    assert isinstance(repository, SQLAlchemyPostRepositoryAdapter)
    assert repository.session is session


def test_build_functions_return_the_expected_use_case_types():
    """Every builder returns a use case wired to the given repository."""
    repository = MagicMock()

    assert isinstance(build_create_post_use_case(repository), CreatePostUseCase)
    assert isinstance(build_get_post_filter_use_case(repository), GetPostFiltersUseCase)
    assert isinstance(build_get_post_by_id_use_case(repository), GetPostUseCase)
    assert isinstance(build_delete_post_use_case(repository), DeletePostUseCase)
    assert isinstance(build_count_posts_use_case(repository), CountPostsUseCase)
    assert isinstance(build_reset_posts_use_case(repository), ResetPostsUseCase)
