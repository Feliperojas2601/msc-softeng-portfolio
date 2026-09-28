from datetime import UTC, datetime
from uuid import uuid4

from domain.models.offer import Offer, OfferSize
from domain.ports.offer_repository_port import OfferRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from entrypoints.api.schemas.create_offer import CreateOffer
from errors import InvalidOfferError

VALID_SIZES = {size.value for size in OfferSize}


class CreateOfferUseCase(BaseUseCase):
    """Use case for saving an offer."""

    def __init__(self, offer_repository: OfferRepositoryPort):
        self.offer_repository = offer_repository

    async def execute(self, data: CreateOffer) -> Offer:
        """Validate business rules and create a new offer."""
        if data.size not in VALID_SIZES:
            raise InvalidOfferError(f"El tamaño '{data.size}' no es válido")

        if data.offer < 0:
            raise InvalidOfferError("El valor de la oferta no puede ser negativo")

        offer = Offer(
            id=str(uuid4()),
            postId=str(data.postId),
            userId=str(data.userId),
            description=data.description,
            size=data.size,
            fragile=data.fragile,
            offer=data.offer,
            createdAt=datetime.now(UTC),
        )

        return await self.offer_repository.create(offer)
