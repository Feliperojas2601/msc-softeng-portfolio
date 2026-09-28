from domain.models.score import Score
from domain.ports.score_repository_port import ScoreRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import ScoreNotFoundError


class GetScoreUseCase(BaseUseCase):
    """Use case for retrieving the score associated with an offer."""

    def __init__(self, score_repository: ScoreRepositoryPort):
        self.score_repository = score_repository

    async def execute(self, offer_id: str) -> Score:
        """Retrieve the score of an offer by its identifier."""
        score = await self.score_repository.get_by_offer_id(offer_id)
        if not score:
            raise ScoreNotFoundError()
        return score
