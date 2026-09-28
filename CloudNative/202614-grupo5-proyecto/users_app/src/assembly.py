from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.database.session import get_session
from adapters.database.user_repository_adapter import SQLAlchemyUserRepositoryAdapter
from adapters.truenative.identity_verification_adapter import (
    TrueNativeIdentityVerificationAdapter,
)
from config import settings
from domain.use_cases.authenticate_user_use_case import AuthenticateUserUseCase
from domain.use_cases.count_users_use_case import CountUsersUseCase
from domain.use_cases.create_user_use_case import CreateUserUseCase
from domain.use_cases.get_current_user_use_case import GetCurrentUserUseCase
from domain.use_cases.get_user_by_id_use_case import GetUserByIdUseCase
from domain.use_cases.reset_users_use_case import ResetUsersUseCase
from domain.use_cases.update_user_use_case import UpdateUserUseCase


def build_user_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLAlchemyUserRepositoryAdapter:
    """Build the user repository adapter bound to a request-scoped session."""
    return SQLAlchemyUserRepositoryAdapter(session)


def build_identity_verification() -> TrueNativeIdentityVerificationAdapter:
    """Build the TrueNative identity verification adapter."""
    return TrueNativeIdentityVerificationAdapter(
        base_url=settings.true_native_base_url,
        secret_token=settings.true_native_secret_token,
    )


def build_create_user_use_case(
    repository: SQLAlchemyUserRepositoryAdapter = Depends(build_user_repository),
    identity_verification: TrueNativeIdentityVerificationAdapter = Depends(
        build_identity_verification
    ),
) -> CreateUserUseCase:
    """Build the create user use case."""
    return CreateUserUseCase(
        repository, identity_verification, settings.true_native_webhook_url
    )


def build_update_user_use_case(
    repository: SQLAlchemyUserRepositoryAdapter = Depends(build_user_repository),
) -> UpdateUserUseCase:
    """Build the update user use case."""
    return UpdateUserUseCase(repository)


def build_authenticate_user_use_case(
    repository: SQLAlchemyUserRepositoryAdapter = Depends(build_user_repository),
) -> AuthenticateUserUseCase:
    """Build the authenticate user use case."""
    return AuthenticateUserUseCase(repository, settings.token_expiration_hours)


def build_get_current_user_use_case(
    repository: SQLAlchemyUserRepositoryAdapter = Depends(build_user_repository),
) -> GetCurrentUserUseCase:
    """Build the get current user use case."""
    return GetCurrentUserUseCase(repository)


def build_get_user_by_id_use_case(
    repository: SQLAlchemyUserRepositoryAdapter = Depends(build_user_repository),
) -> GetUserByIdUseCase:
    """Build the get user by id use case."""
    return GetUserByIdUseCase(repository)


def build_count_users_use_case(
    repository: SQLAlchemyUserRepositoryAdapter = Depends(build_user_repository),
) -> CountUsersUseCase:
    """Build the count users use case."""
    return CountUsersUseCase(repository)


def build_reset_users_use_case(
    repository: SQLAlchemyUserRepositoryAdapter = Depends(build_user_repository),
) -> ResetUsersUseCase:
    """Build the reset users use case."""
    return ResetUsersUseCase(repository)
