from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from domain.models.offer import Offer


class OfferResponse(BaseModel):
    """Response body for GET /offers/{id} and items in GET /offers list."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    post_id: str = Field(alias="postId")
    user_id: str = Field(alias="userId")
    description: str
    size: str
    fragile: bool
    offer: float
    created_at: datetime = Field(alias="createdAt")

    @classmethod
    def from_offer(cls, offer: Offer) -> "OfferResponse":
        """Build a response from a domain Offer."""
        return cls(
            id=offer.id,
            post_id=offer.postId,
            user_id=offer.userId,
            description=offer.description,
            size=offer.size,
            fragile=offer.fragile,
            offer=offer.offer,
            created_at=offer.createdAt,
        )


class MessageResponse(BaseModel):
    """Generic response body containing only a message."""

    msg: str


class CountResponse(BaseModel):
    """Response body for GET /offers/count."""

    count: int
