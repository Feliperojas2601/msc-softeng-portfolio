from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.database.mappers import offer_entity_to_model, offer_model_to_entity
from adapters.database.offer_model import OfferModel
from domain.models.offer import Offer
from domain.ports.offer_repository_port import OfferRepositoryPort
from entrypoints.api.schemas.offer_filters import OfferFilters


class SQLAlchemyOfferRepositoryAdapter(OfferRepositoryPort):
    """PostgreSQL implementation of OfferRepositoryPort using SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, offer: Offer) -> Offer:
        """Persist a new offer."""
        offer_model = offer_entity_to_model(offer)
        self.session.add(offer_model)
        await self.session.commit()
        await self.session.refresh(offer_model)
        return offer_model_to_entity(offer_model)

    async def get_by_id(self, offer_id: str) -> Offer | None:
        """Get offer by ID."""
        result = await self.session.execute(
            select(OfferModel).where(OfferModel.id == offer_id)
        )
        offer_model = result.scalar_one_or_none()
        return offer_model_to_entity(offer_model) if offer_model else None

    async def get_all(self, filters: OfferFilters) -> list[Offer]:
        """Get all offers matching the given filters."""
        query = select(OfferModel)

        if filters.post is not None:
            query = query.where(OfferModel.post_id == filters.post)

        if filters.owner is not None:
            query = query.where(OfferModel.user_id == filters.owner)

        result = await self.session.execute(query)
        offer_models = result.scalars().all()
        return [offer_model_to_entity(model) for model in offer_models]

    async def delete(self, offer_id: str) -> bool:
        """Delete an offer by ID."""
        result = await self.session.execute(
            delete(OfferModel).where(OfferModel.id == offer_id)
        )
        await self.session.commit()
        return result.rowcount > 0

    async def count(self) -> int:
        """Return the total number of offers."""
        result = await self.session.execute(
            select(func.count()).select_from(OfferModel)
        )
        return result.scalar_one()

    async def reset(self) -> None:
        """Delete all offers."""
        await self.session.execute(delete(OfferModel))
        await self.session.commit()
