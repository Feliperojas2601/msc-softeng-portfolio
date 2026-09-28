from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.database.routes_repository_adapter import (
    SQLAlchemyRoutesRepositoryAdapter,
)
from adapters.database.session import get_session
from domain.use_cases.count_routes_use_case import CountRoutesUseCase
from domain.use_cases.create_route_use_case import CreateRouteUseCase
from domain.use_cases.delete_route_use_case import DeleteRouteUseCase
from domain.use_cases.get_route_use_case import GetRouteUseCase
from domain.use_cases.get_routes_use_case import GetRoutesUseCase
from domain.use_cases.reset_routes_use_case import ResetRoutesUseCase


def build_routes_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLAlchemyRoutesRepositoryAdapter:
    """Build a request-scoped routes repository."""
    return SQLAlchemyRoutesRepositoryAdapter(session)


def build_create_route_use_case(
    repository: SQLAlchemyRoutesRepositoryAdapter = Depends(build_routes_repository),
) -> CreateRouteUseCase:
    """Build the create route use case."""
    return CreateRouteUseCase(repository)


def build_get_routes_use_case(
    repository: SQLAlchemyRoutesRepositoryAdapter = Depends(build_routes_repository),
) -> GetRoutesUseCase:
    """Build the list routes use case."""
    return GetRoutesUseCase(repository)


def build_get_route_use_case(
    repository: SQLAlchemyRoutesRepositoryAdapter = Depends(build_routes_repository),
) -> GetRouteUseCase:
    """Build the get route use case."""
    return GetRouteUseCase(repository)


def build_delete_route_use_case(
    repository: SQLAlchemyRoutesRepositoryAdapter = Depends(build_routes_repository),
) -> DeleteRouteUseCase:
    """Build the delete route use case."""
    return DeleteRouteUseCase(repository)


def build_count_routes_use_case(
    repository: SQLAlchemyRoutesRepositoryAdapter = Depends(build_routes_repository),
) -> CountRoutesUseCase:
    """Build the count routes use case."""
    return CountRoutesUseCase(repository)


def build_reset_routes_use_case(
    repository: SQLAlchemyRoutesRepositoryAdapter = Depends(build_routes_repository),
) -> ResetRoutesUseCase:
    """Build the reset routes use case."""
    return ResetRoutesUseCase(repository)
