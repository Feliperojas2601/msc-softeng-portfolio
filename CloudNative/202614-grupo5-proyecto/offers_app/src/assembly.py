from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.database.postgres_offer_repository import SQLAlchemyOfferRepositoryAdapter
from adapters.database.session import get_session
from domain.use_cases.count_offers_use_case import CountOffersUseCase
from domain.use_cases.create_offer_use_case import CreateOfferUseCase
from domain.use_cases.delete_offer_use_case import DeleteOfferUseCase
from domain.use_cases.get_offer_filter_use_case import GetOfferFiltersUseCase
from domain.use_cases.get_offer_use_case import GetOfferUseCase
from domain.use_cases.reset_offers_use_case import ResetOffersUseCase


def build_offer_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLAlchemyOfferRepositoryAdapter:
    """Build the offer repository adapter bound to a request-scoped session."""
    return SQLAlchemyOfferRepositoryAdapter(session)


def build_create_offer_use_case(
    repository: SQLAlchemyOfferRepositoryAdapter = Depends(build_offer_repository),
) -> CreateOfferUseCase:
    """Build the create offer use case."""
    return CreateOfferUseCase(repository)


def build_get_offer_filter_use_case(
    repository: SQLAlchemyOfferRepositoryAdapter = Depends(build_offer_repository),
) -> GetOfferFiltersUseCase:
    """Build the search offers use case."""
    return GetOfferFiltersUseCase(repository)


def build_get_offer_by_id_use_case(
    repository: SQLAlchemyOfferRepositoryAdapter = Depends(build_offer_repository),
) -> GetOfferUseCase:
    """Build the get offer by id use case."""
    return GetOfferUseCase(repository)


def build_delete_offer_use_case(
    repository: SQLAlchemyOfferRepositoryAdapter = Depends(build_offer_repository),
) -> DeleteOfferUseCase:
    """Build the delete offer use case."""
    return DeleteOfferUseCase(repository)


def build_count_offers_use_case(
    repository: SQLAlchemyOfferRepositoryAdapter = Depends(build_offer_repository),
) -> CountOffersUseCase:
    """Build the count offers use case."""
    return CountOffersUseCase(repository)


def build_reset_offers_use_case(
    repository: SQLAlchemyOfferRepositoryAdapter = Depends(build_offer_repository),
) -> ResetOffersUseCase:
    """Build the reset offers use case."""
    return ResetOffersUseCase(repository)
