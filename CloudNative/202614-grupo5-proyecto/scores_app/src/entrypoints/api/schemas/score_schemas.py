from pydantic import BaseModel, ConfigDict, Field

from domain.models.score import Score


class ScoreResponse(BaseModel):
    """Response body for GET /scores/{offerId}."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    offer_id: str = Field(alias="offerId")
    size: str
    offer: float
    bag_cost: float = Field(alias="bagCost")
    utility: float
    created_at: str = Field(alias="createdAt")

    @classmethod
    def from_score(cls, score: Score) -> "ScoreResponse":
        """Build a response from a domain Score."""
        return cls(
            id=score.id,
            offer_id=score.offerId,
            size=score.size,
            offer=score.offer,
            bag_cost=score.bagCost,
            utility=score.utility,
            created_at=score.createdAt.isoformat(),
        )
