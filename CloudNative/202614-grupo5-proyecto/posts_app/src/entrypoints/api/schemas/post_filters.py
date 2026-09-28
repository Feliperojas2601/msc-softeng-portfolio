from pydantic import BaseModel, Field


class PostFilters(BaseModel):
    """Filters used to search posts."""

    expire: bool | None = Field(
        default=None,
        description="Filtrar publicaciones por estado de caducidad",
    )
    route: str | None = Field(
        default=None,
        min_length=1,
        description="Identificador de ruta",
    )
    owner: str | None = Field(
        default=None,
        min_length=1,
        description="Identificador del usuario propietario de la publicación",
    )
