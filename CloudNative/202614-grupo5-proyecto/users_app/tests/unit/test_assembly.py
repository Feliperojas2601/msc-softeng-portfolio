from unittest.mock import MagicMock

from adapters.database.user_repository_adapter import SQLAlchemyUserRepositoryAdapter
from assembly import (
    build_authenticate_user_use_case,
    build_count_users_use_case,
    build_create_user_use_case,
    build_get_current_user_use_case,
    build_get_user_by_id_use_case,
    build_reset_users_use_case,
    build_update_user_use_case,
    build_user_repository,
)
from domain.use_cases.authenticate_user_use_case import AuthenticateUserUseCase
from domain.use_cases.count_users_use_case import CountUsersUseCase
from domain.use_cases.create_user_use_case import CreateUserUseCase
from domain.use_cases.get_current_user_use_case import GetCurrentUserUseCase
from domain.use_cases.get_user_by_id_use_case import GetUserByIdUseCase
from domain.use_cases.reset_users_use_case import ResetUsersUseCase
from domain.use_cases.update_user_use_case import UpdateUserUseCase


def test_build_user_repository_wraps_the_given_session():
    """build_user_repository binds the injected session to the adapter."""
    session = MagicMock()

    repository = build_user_repository(session)

    assert isinstance(repository, SQLAlchemyUserRepositoryAdapter)
    assert repository.session is session


def test_build_functions_return_the_expected_use_case_types():
    """Every builder returns a use case wired to the given repository."""
    repository = MagicMock()

    assert isinstance(build_create_user_use_case(repository), CreateUserUseCase)
    assert isinstance(build_update_user_use_case(repository), UpdateUserUseCase)
    assert isinstance(
        build_authenticate_user_use_case(repository), AuthenticateUserUseCase
    )
    assert isinstance(
        build_get_current_user_use_case(repository), GetCurrentUserUseCase
    )
    assert isinstance(build_count_users_use_case(repository), CountUsersUseCase)
    assert isinstance(build_reset_users_use_case(repository), ResetUsersUseCase)
    assert isinstance(build_get_user_by_id_use_case(repository), GetUserByIdUseCase)
