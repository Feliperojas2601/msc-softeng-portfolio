from domain.models.offer import Offer
from domain.ports.offer_repository_port import OfferRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import OfferNotFoundError


class GetOfferUseCase(BaseUseCase):
    """Use case for retrieving an offer by its identifier."""

    def __init__(self, offer_repository: OfferRepositoryPort):
        self.offer_repository = offer_repository

    async def execute(self, offer_id: str) -> Offer:
        """Retrieve an offer by its identifier."""
        offer = await self.offer_repository.get_by_id(offer_id)
        if not offer:
            raise OfferNotFoundError()
        return offer
