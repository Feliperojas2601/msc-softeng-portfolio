from datetime import UTC, datetime
from uuid import uuid4

from domain.models.score import Score, ScoreSize
from domain.ports.score_repository_port import ScoreRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from entrypoints.api.schemas.create_score import CreateScore
from errors import InvalidScoreError

OCCUPANCY = {
    ScoreSize.LARGE: 1.0,
    ScoreSize.MEDIUM: 0.5,
    ScoreSize.SMALL: 0.25,
}


class CreateScoreUseCase(BaseUseCase):
    """Use case for calculating and persisting the utility (score) of an offer."""

    def __init__(self, score_repository: ScoreRepositoryPort):
        self.score_repository = score_repository

    async def execute(self, data: CreateScore) -> Score:
        """Calculate the utility from the offer's inputs and persist the score."""
        if data.size not in {size.value for size in ScoreSize}:
            raise InvalidScoreError(f"El tamaño '{data.size}' no es válido")

        occupancy = OCCUPANCY[ScoreSize(data.size)]
        utility = data.offer - (occupancy * data.bagCost)

        score = Score(
            id=str(uuid4()),
            offerId=data.offerId,
            size=data.size,
            offer=data.offer,
            bagCost=data.bagCost,
            utility=utility,
            createdAt=datetime.now(UTC),
        )

        return await self.score_repository.create(score)
