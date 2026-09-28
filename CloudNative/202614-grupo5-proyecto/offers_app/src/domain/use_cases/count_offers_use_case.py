from domain.ports.offer_repository_port import OfferRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class CountOffersUseCase(BaseUseCase):
    """Use case for counting offers."""

    def __init__(self, offer_repository: OfferRepositoryPort):
        self.offer_repository = offer_repository

    async def execute(self) -> int:
        """Return the number of offers."""
        return await self.offer_repository.count()
