from datetime import datetime

from pydantic import BaseModel, Field

from domain.models.airport_code import AirportCode
from domain.models.route import Route


class CreateRouteRequest(BaseModel):
    """Request body for POST /routes."""

    flightId: str = Field(min_length=1)
    sourceAirportCode: AirportCode
    sourceCountry: str = Field(min_length=1)
    destinyAirportCode: AirportCode
    destinyCountry: str = Field(min_length=1)
    bagCost: int = Field(ge=0)
    plannedStartDate: datetime
    plannedEndDate: datetime


class CreateRouteResponse(BaseModel):
    """Response body for POST /routes."""

    id: str
    createdAt: datetime

    @classmethod
    def from_route(cls, route: Route) -> "CreateRouteResponse":
        """Build a response from a domain route."""
        return cls(id=route.id, createdAt=route.created_at)


class RouteResponse(BaseModel):
    """Complete public representation of a route."""

    id: str
    flightId: str
    sourceAirportCode: AirportCode
    sourceCountry: str
    destinyAirportCode: AirportCode
    destinyCountry: str
    bagCost: int = Field(ge=0)
    plannedStartDate: datetime
    plannedEndDate: datetime
    createdAt: datetime
    updatedAt: datetime

    @classmethod
    def from_route(cls, route: Route) -> "RouteResponse":
        """Build a response from a domain route."""
        return cls(
            id=route.id,
            flightId=route.flight_id,
            sourceAirportCode=route.source_airport_code,
            sourceCountry=route.source_country,
            destinyAirportCode=route.destiny_airport_code,
            destinyCountry=route.destiny_country,
            bagCost=route.bag_cost,
            plannedStartDate=route.planned_start_date,
            plannedEndDate=route.planned_end_date,
            createdAt=route.created_at,
            updatedAt=route.updated_at,
        )


class CountResponse(BaseModel):
    """Response body for GET /routes/count."""

    count: int = Field(ge=0)


class MessageResponse(BaseModel):
    """Generic message response."""

    msg: str
