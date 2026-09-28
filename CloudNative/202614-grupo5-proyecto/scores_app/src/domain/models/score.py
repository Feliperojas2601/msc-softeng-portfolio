from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ScoreSize(str, Enum):

    LARGE = "LARGE"
    MEDIUM = "MEDIUM"
    SMALL = "SMALL"


class Score(BaseModel):
    """Utilidad (score) calculada y persistida para una oferta."""

    id: str = Field(min_length=1, description="Identificador del score en formato UUID")
    offerId: str = Field(min_length=1, description="Identificador de la oferta asociada")
    size: str = Field(
        min_length=1, description="Tamaño del paquete: LARGE, MEDIUM o SMALL"
    )
    offer: float = Field(description="Valor en dólares que se propuso por el envío")
    bagCost: float = Field(description="Costo de la maleta en el trayecto")
    utility: float = Field(description="Utilidad calculada de la oferta")
    createdAt: datetime
