from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class OfferSize(str, Enum):
    """Tamaño del paquete a llevar, como se define en offers_app."""

    LARGE = "LARGE"
    MEDIUM = "MEDIUM"
    SMALL = "SMALL"


class CreateOfferCommand(BaseModel):
    """Interfaz de comando para crear una oferta"""

    model_config = ConfigDict(populate_by_name=True)

    description: str = Field(
        min_length=1, description="Descripción del paquete a llevar"
    )
    size: OfferSize = Field(description="Tamaño del paquete")
    fragile: bool = Field(description="Indica si el paquete es delicado")
    offer: float = Field(description="Valor en dólares que se propone por el envío")


class CreatedOffer(BaseModel):
    """Representa una oferta creada, como la devuelve offers_app."""

    id: str = Field(min_length=1, description="Identificador de la oferta creada")
    user_id: str = Field(min_length=1, description="Identificador del usuario dueño")
    created_at: datetime = Field(description="Fecha y hora de creación de la oferta")


class Offer(BaseModel):
    """Una oferta completa sobre una publicación, como la devuelve offers_app."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(min_length=1, description="Identificador de la oferta")
    user_id: str = Field(
        min_length=1, description="Identificador del usuario que hizo la oferta"
    )
    description: str = Field(description="Descripción del paquete a llevar")
    size: OfferSize = Field(description="Tamaño del paquete")
    fragile: bool = Field(description="Indica si el paquete es delicado")
    offer: float = Field(description="Valor en dólares de la oferta")
    created_at: datetime = Field(description="Fecha y hora de creación de la oferta")
