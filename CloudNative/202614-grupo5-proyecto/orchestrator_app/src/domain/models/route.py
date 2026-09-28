from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Route(BaseModel):
    """Una ruta de envío, como la devuelve routes_app."""

    id: str = Field(min_length=1, description="Identificador del trayecto")
    bag_cost: float = Field(
        ge=0, description="Costo de envio de una maleta en el trayecto, en dolares"
    )


class RouteDetail(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    flight_id: str = Field(..., alias="flightId")
    source_airport_code: str = Field(..., alias="sourceAirportCode")
    source_country: str = Field(..., alias="sourceCountry")
    destiny_airport_code: str = Field(..., alias="destinyAirportCode")
    destiny_country: str = Field(..., alias="destinyCountry")
    bag_cost: float = Field(..., alias="bagCost")
    planned_start_date: datetime | None = Field(default=None, alias="plannedStartDate")
    planned_end_date: datetime | None = Field(default=None, alias="plannedEndDate")
    created_at: datetime = Field(..., alias="createdAt")


class CreatedRoute(BaseModel):
    """Representa el resultado de la creación de una ruta."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    created_at: datetime = Field(..., alias="createdAt")
