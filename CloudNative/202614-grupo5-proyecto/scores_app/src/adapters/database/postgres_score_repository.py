from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.database.mappers import score_entity_to_model, score_model_to_entity
from adapters.database.score_model import ScoreModel
from domain.models.score import Score
from domain.ports.score_repository_port import ScoreRepositoryPort


class SQLAlchemyScoreRepositoryAdapter(ScoreRepositoryPort):
    """PostgreSQL implementation of ScoreRepositoryPort using SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, score: Score) -> Score:
        """Persist a new score."""
        score_model = score_entity_to_model(score)
        self.session.add(score_model)
        await self.session.commit()
        await self.session.refresh(score_model)
        return score_model_to_entity(score_model)

    async def get_by_offer_id(self, offer_id: str) -> Score | None:
        """Get the score associated with an offer, if it has been calculated."""
        result = await self.session.execute(
            select(ScoreModel).where(ScoreModel.offer_id == offer_id)
        )
        score_model = result.scalar_one_or_none()
        return score_model_to_entity(score_model) if score_model else None
