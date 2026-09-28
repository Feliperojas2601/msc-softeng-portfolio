from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from domain.models.offer import Offer


class CreateOffer(BaseModel):
    """Request body for POST /offers."""

    model_config = ConfigDict(populate_by_name=True)

    postId: UUID = Field(..., description="ID de la publicación en formato UUID")
    userId: UUID = Field(
        ..., description="ID del usuario dueño de la oferta en formato UUID"
    )
    description: str = Field(
        ..., min_length=1, description="Descripción del paquete a llevar"
    )
    size: str = Field(
        ..., min_length=1, description="Tamaño del paquete: LARGE, MEDIUM o SMALL"
    )
    fragile: bool = Field(..., description="Indica si el paquete es delicado")
    offer: float = Field(..., description="Valor en dólares de la oferta")


class CreateOfferResponse(BaseModel):
    """Response body for POST /offers."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    user_id: str = Field(alias="userId")
    created_at: datetime = Field(alias="createdAt")

    @classmethod
    def from_offer(cls, offer: Offer) -> "CreateOfferResponse":
        """Build a response from a domain Offer."""
        return cls(
            id=offer.id,
            user_id=offer.userId,
            created_at=offer.createdAt,
        )
