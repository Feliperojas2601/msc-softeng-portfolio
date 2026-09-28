from pydantic import BaseModel, ConfigDict, Field

from domain.models.score import Score


class CreateScore(BaseModel):
    """Request body for POST /scores."""

    model_config = ConfigDict(populate_by_name=True)

    offerId: str = Field(min_length=1, description="Identificador de la oferta")
    size: str = Field(
        min_length=1, description="Tamaño del paquete: LARGE, MEDIUM o SMALL"
    )
    offer: float = Field(description="Valor en dólares que se propuso por el envío")
    bagCost: float = Field(description="Costo de la maleta en el trayecto")


class CreateScoreResponse(BaseModel):
    """Response body for POST /scores."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    offer_id: str = Field(alias="offerId")
    size: str
    offer: float
    bag_cost: float = Field(alias="bagCost")
    utility: float
    created_at: str = Field(alias="createdAt")

    @classmethod
    def from_score(cls, score: Score) -> "CreateScoreResponse":
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
