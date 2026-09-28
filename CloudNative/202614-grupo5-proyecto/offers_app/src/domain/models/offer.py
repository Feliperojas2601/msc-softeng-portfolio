from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class OfferSize(str, Enum):

    LARGE = "LARGE"
    MEDIUM = "MEDIUM"
    SMALL = "SMALL"


class Offer(BaseModel):

    id: str = Field(
        min_length=1, description="Identificador de la oferta en formato UUID"
    )
    postId: str = Field(min_length=1, description="Identificador de la publicación")
    userId: str = Field(
        min_length=1, description="Identificador del usuario dueño de la oferta"
    )
    description: str = Field(
        min_length=1, description="Descripción del paquete a llevar"
    )
    size: str = Field(
        min_length=1, description="Tamaño del paquete: LARGE, MEDIUM o SMALL"
    )
    fragile: bool = Field(description="Indica si el paquete es delicado")
    offer: float = Field(description="Valor en dólares de la oferta")
    createdAt: datetime
