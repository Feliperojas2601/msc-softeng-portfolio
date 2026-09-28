from domain.models.offer import Offer
from domain.ports.offer_repository_port import OfferRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from entrypoints.api.schemas.offer_filters import OfferFilters


class GetOfferFiltersUseCase(BaseUseCase):
    """Use case for searching offers."""

    def __init__(self, offer_repository: OfferRepositoryPort):
        self.offer_repository = offer_repository

    async def execute(self, filters: OfferFilters) -> list[Offer]:
        """Return offers matching the provided filters."""
        return await self.offer_repository.get_all(filters)
