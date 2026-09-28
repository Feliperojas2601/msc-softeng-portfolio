from domain.ports.offer_repository_port import OfferRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import OfferNotFoundError


class DeleteOfferUseCase(BaseUseCase):
    """Use case for deleting an offer."""

    def __init__(self, offer_repository: OfferRepositoryPort):
        self.offer_repository = offer_repository

    async def execute(self, offer_id: str) -> bool:
        """Delete an offer by its identifier."""
        deleted = await self.offer_repository.delete(offer_id)
        if not deleted:
            raise OfferNotFoundError()

        return deleted
