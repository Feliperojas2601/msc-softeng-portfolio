from abc import ABC, abstractmethod

from domain.models.score import Score


class ScoreRepositoryPort(ABC):
    """Score repository interface."""

    @abstractmethod
    async def create(self, score: Score) -> Score:
        """Persist a new score."""

    @abstractmethod
    async def get_by_offer_id(self, offer_id: str) -> Score | None:
        """Get the score associated with an offer, if it has been calculated."""
