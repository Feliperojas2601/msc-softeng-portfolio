from pydantic import BaseModel, Field


class OfferFilters(BaseModel):
    """Filters used to search offers."""

    post: str | None = Field(
        default=None,
        min_length=1,
        description="Identificador de la publicación que se desea usar para el envío",
    )
    owner: str | None = Field(
        default=None,
        min_length=1,
        description="Identificador del usuario dueño de la oferta",
    )
