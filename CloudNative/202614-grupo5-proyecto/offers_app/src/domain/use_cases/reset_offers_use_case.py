from domain.ports.offer_repository_port import OfferRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase


class ResetOffersUseCase(BaseUseCase):
    """Use case for resetting the offers database."""

    def __init__(self, offer_repository: OfferRepositoryPort):
        self.offer_repository = offer_repository

    async def execute(self) -> None:
        """Delete all offers."""
        await self.offer_repository.reset()
