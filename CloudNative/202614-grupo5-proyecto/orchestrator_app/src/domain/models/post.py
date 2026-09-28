from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Post(BaseModel):
    """Representa una publicación de envío, como la devuelve posts_app."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(min_length=1, description="Identificador de la publicación")
    route_id: str = Field(
        min_length=1, description="Identificador del trayecto asociado"
    )
    user_id: str = Field(min_length=1, description="Identificador del usuario dueño")
    expire_at: datetime = Field(
        description="Fecha y hora máxima en la que se reciben ofertas (UTC)"
    )
    created_at: datetime = Field(
        description="Fecha y hora de creación de la publicación"
    )


class Location(BaseModel):
    """Modelo para representar la ubicación de origen o destino."""

    model_config = ConfigDict(populate_by_name=True)

    airport_code: str = Field(
        ...,
        alias="airportCode",
        json_schema_extra={"example": "BOG"},
        description="Código IATA del aeropuerto",
    )
    country: str = Field(
        ...,
        json_schema_extra={"example": "Colombia"},
        description="Nombre del país",
    )


class CreatePostCommand(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    flight_id: str
    expire_at: datetime
    planned_start_date: datetime
    planned_end_date: datetime
    origin: Location
    destiny: Location
    bag_cost: float


class CreatePost(BaseModel):
    """Response body for POST /posts."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    user_id: str = Field(alias="userId")
    created_at: datetime = Field(alias="createdAt")


class CreatedRouteSummary(BaseModel):
    """Representa el resumen de la ruta dentro de la respuesta de la publicación."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    created_at: datetime = Field(..., alias="createdAt")


class CreatedPostResponse(BaseModel):
    """Representa la respuesta completa de creación de una publicación para RF-003."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    user_id: str = Field(..., alias="userId")
    created_at: datetime = Field(..., alias="createdAt")
    expire_at: datetime = Field(..., alias="expireAt")
    route: CreatedRouteSummary
