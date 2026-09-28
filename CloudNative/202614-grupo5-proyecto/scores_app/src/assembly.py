from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.database.postgres_score_repository import SQLAlchemyScoreRepositoryAdapter
from adapters.database.session import get_session
from domain.use_cases.create_score_use_case import CreateScoreUseCase
from domain.use_cases.get_score_use_case import GetScoreUseCase


def build_score_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLAlchemyScoreRepositoryAdapter:
    """Build the score repository adapter bound to a request-scoped session."""
    return SQLAlchemyScoreRepositoryAdapter(session)


def build_create_score_use_case(
    repository: SQLAlchemyScoreRepositoryAdapter = Depends(build_score_repository),
) -> CreateScoreUseCase:
    """Build the create score use case."""
    return CreateScoreUseCase(repository)


def build_get_score_use_case(
    repository: SQLAlchemyScoreRepositoryAdapter = Depends(build_score_repository),
) -> GetScoreUseCase:
    """Build the get score use case."""
    return GetScoreUseCase(repository)
