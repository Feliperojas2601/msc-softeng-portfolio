from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from domain.models.offer import CreatedOffer, CreateOfferCommand, OfferSize


class CreateOfferRequest(BaseModel):
    """Request body para ``POST /rf004/posts/{id}/offers``."""

    model_config = ConfigDict(populate_by_name=True)

    description: str = Field(
        min_length=1, description="Descripción del paquete a llevar"
    )
    size: OfferSize = Field(description="Tamaño del paquete: LARGE, MEDIUM o SMALL")
    fragile: bool = Field(description="Indica si el paquete es delicado")
    offer: float = Field(description="Valor en dólares que se propone por el envío")

    def to_command(self) -> CreateOfferCommand:
        """Map the request into the domain command consumed by the use case."""
        return CreateOfferCommand(
            description=self.description,
            size=self.size,
            fragile=self.fragile,
            offer=self.offer,
        )


class Rf004Data(BaseModel):
    """Objeto data de respuesta de RF-004."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    user_id: str = Field(alias="userId")
    created_at: datetime = Field(alias="createdAt")
    post_id: str = Field(alias="postId")


class Rf004Response(BaseModel):
    """Respuesta de RF-004."""

    model_config = ConfigDict(populate_by_name=True)

    data: Rf004Data
    msg: str

    @classmethod
    def from_offer(cls, offer: CreatedOffer, post_id: str) -> "Rf004Response":
        """Construye la respuesta a partir de la oferta creada y el ID de la publicación."""
        return cls(
            data=Rf004Data(
                id=offer.id,
                user_id=offer.user_id,
                created_at=offer.created_at,
                post_id=post_id,
            ),
            msg=f"Oferta {offer.id} creada para la publicación {post_id}",
        )
