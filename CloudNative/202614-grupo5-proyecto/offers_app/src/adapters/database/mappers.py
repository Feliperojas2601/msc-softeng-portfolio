from adapters.database.offer_model import OfferModel
from domain.models.offer import Offer


def offer_entity_to_model(offer: Offer) -> OfferModel:
    """Map Offer domain entity to SQLAlchemy OfferModel."""
    return OfferModel(
        id=offer.id,
        post_id=offer.postId,
        user_id=offer.userId,
        description=offer.description,
        size=offer.size,
        fragile=offer.fragile,
        offer=offer.offer,
        created_at=offer.createdAt,
    )


def offer_model_to_entity(model: OfferModel) -> Offer:
    """Map SQLAlchemy OfferModel to Offer domain entity."""
    return Offer(
        id=model.id,
        postId=model.post_id,
        userId=model.user_id,
        description=model.description,
        size=model.size,
        fragile=model.fragile,
        offer=model.offer,
        createdAt=model.created_at,
    )
