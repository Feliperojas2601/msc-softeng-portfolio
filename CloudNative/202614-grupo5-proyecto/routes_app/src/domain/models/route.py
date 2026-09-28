from datetime import datetime

from pydantic import BaseModel, Field

from domain.models.airport_code import AirportCode


class Route(BaseModel):
    """Route domain model independent from HTTP and database details."""

    id: str
    flight_id: str = Field(min_length=1)
    source_airport_code: AirportCode
    source_country: str = Field(min_length=1)
    destiny_airport_code: AirportCode
    destiny_country: str = Field(min_length=1)
    bag_cost: int = Field(ge=0)
    planned_start_date: datetime
    planned_end_date: datetime
    created_at: datetime
    updated_at: datetime
