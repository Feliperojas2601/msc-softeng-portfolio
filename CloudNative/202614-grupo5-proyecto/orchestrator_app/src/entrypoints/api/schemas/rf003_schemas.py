from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from domain.models.post import CreatedPostResponse, CreatePostCommand, Location


class LocationData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    airportCode: str = Field(
        ...,
        json_schema_extra={"example": "BOG"},
        description="Código IATA del aeropuerto",
    )
    country: str = Field(
        ..., json_schema_extra={"example": "Colombia"}, description="Nombre del país"
    )


class CreatePublicationRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    flightId: str = Field(
        ...,
        json_schema_extra={"example": "FL-12345"},
        description="Identificador del vuelo",
    )
    expireAt: datetime = Field(
        ...,
        json_schema_extra={"example": "2026-09-10T23:59:59Z"},
        description="Fecha y hora máxima para recibir ofertas (ISO)",
    )
    plannedStartDate: datetime = Field(
        ...,
        json_schema_extra={"example": "2026-09-12T08:00:00Z"},
        description="Fecha planeada de salida en formato ISO",
    )
    plannedEndDate: datetime = Field(
        ...,
        json_schema_extra={"example": "2026-09-12T12:00:00Z"},
        description="Fecha planeada de llegada en formato ISO",
    )
    origin: LocationData = Field(..., description="Información del origen")
    destiny: LocationData = Field(..., description="Información del destino")
    bagCost: float = Field(
        ...,
        ge=0,
        json_schema_extra={"example": 25.50},
        description="Costo de envío de maleta en dólares",
    )

    def to_command(self) -> CreatePostCommand:
        """Mapea la solicitud HTTP estructurada al comando de dominio."""
        return CreatePostCommand(
            flight_id=self.flightId,
            expire_at=self.expireAt,
            planned_start_date=self.plannedStartDate,
            planned_end_date=self.plannedEndDate,
            origin=Location(
                airport_code=self.origin.airportCode,
                country=self.origin.country,
            ),
            destiny=Location(
                airport_code=self.destiny.airportCode,
                country=self.destiny.country,
            ),
            bag_cost=self.bagCost,
        )


class RouteData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., json_schema_extra={"example": "ROT-987"})
    createdAt: datetime = Field(
        ..., json_schema_extra={"example": "2026-09-03T14:00:00Z"}
    )


class PublicationData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., json_schema_extra={"example": "PUB-555"})
    userId: str = Field(..., json_schema_extra={"example": "USR-001"})
    createdAt: datetime = Field(
        ..., json_schema_extra={"example": "2026-09-03T14:00:00Z"}
    )
    expireAt: datetime = Field(
        ..., json_schema_extra={"example": "2026-09-10T23:59:59Z"}
    )
    route: RouteData


class Rf003Response(BaseModel):
    data: PublicationData
    msg: str = Field(
        ..., json_schema_extra={"example": "La publicación se ha creado exitosamente."}
    )

    @classmethod
    def from_publication(cls, data: CreatedPostResponse) -> "Rf003Response":
        """Construye la respuesta de éxito a partir de los datos de la publicación creada."""
        return cls(
            data=PublicationData(
                id=data.id,
                userId=data.user_id,
                createdAt=data.created_at,
                expireAt=data.expire_at,
                route=RouteData(
                    id=data.route.id,
                    createdAt=data.route.created_at,
                ),
            ),
            msg=f"Publicación {data.id} creada exitosamente.",
        )


class MessageResponse(BaseModel):
    msg: str
