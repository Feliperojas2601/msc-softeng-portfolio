from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from domain.models.airport_code import AirportCode
from domain.models.route import Route
from domain.ports.routes_repository_port import RoutesRepositoryPort

ROUTE_ID = "a3f1c2d4-0000-4000-8000-000000000001"


@pytest.fixture
def route_data() -> dict:
    """Valid route values accepted by the public API."""
    return {
        "flightId": "FL-001",
        "sourceAirportCode": "BOG",
        "sourceCountry": "Colombia",
        "destinyAirportCode": "MEX",
        "destinyCountry": "México",
        "bagCost": 120,
        "plannedStartDate": "2099-01-01T10:00:00",
        "plannedEndDate": "2099-01-01T14:00:00",
    }


@pytest.fixture
def existing_route() -> Route:
    """A complete route as returned by a repository."""
    now = datetime(2026, 1, 1, 12, 0, 0)
    return Route(
        id=ROUTE_ID,
        flight_id="FL-001",
        source_airport_code=AirportCode.BOG,
        source_country="Colombia",
        destiny_airport_code=AirportCode.MEX,
        destiny_country="México",
        bag_cost=120,
        planned_start_date=datetime(2099, 1, 1, 10, 0, 0),
        planned_end_date=datetime(2099, 1, 1, 14, 0, 0),
        created_at=now,
        updated_at=now,
    )


@pytest.fixture
def mock_routes_repository() -> AsyncMock:
    """A mocked implementation of the domain repository port."""
    return AsyncMock(spec=RoutesRepositoryPort)
