from unittest.mock import MagicMock

from adapters.database.postgres_offer_repository import SQLAlchemyOfferRepositoryAdapter
from assembly import (
    build_count_offers_use_case,
    build_create_offer_use_case,
    build_delete_offer_use_case,
    build_get_offer_by_id_use_case,
    build_get_offer_filter_use_case,
    build_offer_repository,
    build_reset_offers_use_case,
)
from domain.use_cases.count_offers_use_case import CountOffersUseCase
from domain.use_cases.create_offer_use_case import CreateOfferUseCase
from domain.use_cases.delete_offer_use_case import DeleteOfferUseCase
from domain.use_cases.get_offer_filter_use_case import GetOfferFiltersUseCase
from domain.use_cases.get_offer_use_case import GetOfferUseCase
from domain.use_cases.reset_offers_use_case import ResetOffersUseCase


def test_build_offer_repository_wraps_the_given_session():
    """build_offer_repository binds the injected session to the adapter."""
    session = MagicMock()

    repository = build_offer_repository(session)

    assert isinstance(repository, SQLAlchemyOfferRepositoryAdapter)
    assert repository.session is session


def test_build_functions_return_the_expected_use_case_types():
    """Every builder returns a use case wired to the given repository."""
    repository = MagicMock()

    assert isinstance(build_create_offer_use_case(repository), CreateOfferUseCase)
    assert isinstance(
        build_get_offer_filter_use_case(repository), GetOfferFiltersUseCase
    )
    assert isinstance(build_get_offer_by_id_use_case(repository), GetOfferUseCase)
    assert isinstance(build_delete_offer_use_case(repository), DeleteOfferUseCase)
    assert isinstance(build_count_offers_use_case(repository), CountOffersUseCase)
    assert isinstance(build_reset_offers_use_case(repository), ResetOffersUseCase)
