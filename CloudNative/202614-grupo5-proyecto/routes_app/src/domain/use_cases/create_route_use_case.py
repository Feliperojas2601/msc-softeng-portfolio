import uuid
from datetime import datetime, timezone

from domain.models.airport_code import AirportCode
from domain.models.route import Route
from domain.ports.routes_repository_port import RoutesRepositoryPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import InvalidRouteDatesError, RouteAlreadyExistsError


def utcnow() -> datetime:
    """Return a timezone-naive UTC timestamp for storage and API output."""
    return datetime.now(timezone.utc).replace(tzinfo=None, microsecond=0)


def as_utc_naive(value: datetime) -> datetime:
    """Normalize aware or naive input datetimes to timezone-naive UTC."""
    if value.tzinfo is None:
        return value.replace(microsecond=0)
    return value.astimezone(timezone.utc).replace(tzinfo=None, microsecond=0)


class CreateRouteUseCase(BaseUseCase):
    """Create a unique route for a future flight."""

    def __init__(self, route_repository: RoutesRepositoryPort):
        self.route_repository = route_repository

    async def execute(
        self,
        flight_id: str,
        source_airport_code: AirportCode,
        source_country: str,
        destiny_airport_code: AirportCode,
        destiny_country: str,
        bag_cost: int,
        planned_start_date: datetime,
        planned_end_date: datetime,
    ) -> Route:
        """Validate and persist a route."""
        if await self.route_repository.get_by_flight_id(flight_id):
            raise RouteAlreadyExistsError()

        start = as_utc_naive(planned_start_date)
        end = as_utc_naive(planned_end_date)
        now = utcnow()
        if start <= now or end <= now or end <= start:
            raise InvalidRouteDatesError()

        route = Route(
            id=str(uuid.uuid4()),
            flight_id=flight_id,
            source_airport_code=source_airport_code,
            source_country=source_country,
            destiny_airport_code=destiny_airport_code,
            destiny_country=destiny_country,
            bag_cost=bag_cost,
            planned_start_date=start,
            planned_end_date=end,
            created_at=now,
            updated_at=now,
        )
        return await self.route_repository.create(route)
