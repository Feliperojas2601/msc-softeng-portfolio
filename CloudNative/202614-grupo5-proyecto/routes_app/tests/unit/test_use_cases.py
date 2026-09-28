from datetime import datetime, timedelta, timezone

import pytest

from domain.models.airport_code import AirportCode
from domain.use_cases.count_routes_use_case import CountRoutesUseCase
from domain.use_cases.create_route_use_case import (
    CreateRouteUseCase,
    as_utc_naive,
    utcnow,
)
from domain.use_cases.delete_route_use_case import DeleteRouteUseCase
from domain.use_cases.get_route_use_case import GetRouteUseCase
from domain.use_cases.get_routes_use_case import GetRoutesUseCase
from domain.use_cases.reset_routes_use_case import ResetRoutesUseCase
from errors import InvalidRouteDatesError, RouteAlreadyExistsError, RouteNotFoundError


def create_arguments(start: datetime, end: datetime) -> dict:
    """Build arguments for CreateRouteUseCase."""
    return {
        "flight_id": "FL-001",
        "source_airport_code": AirportCode.BOG,
        "source_country": "Colombia",
        "destiny_airport_code": AirportCode.MEX,
        "destiny_country": "México",
        "bag_cost": 120,
        "planned_start_date": start,
        "planned_end_date": end,
    }


@pytest.mark.asyncio
async def test_create_route_success(mock_routes_repository):
    now = datetime.now(timezone.utc)
    start = now + timedelta(days=2)
    end = start + timedelta(hours=4)
    mock_routes_repository.get_by_flight_id.return_value = []
    mock_routes_repository.create.side_effect = lambda route: route

    route = await CreateRouteUseCase(mock_routes_repository).execute(
        **create_arguments(start, end)
    )

    assert route.flight_id == "FL-001"
    assert route.source_airport_code is AirportCode.BOG
    assert route.planned_start_date.tzinfo is None
    mock_routes_repository.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_route_rejects_duplicate(mock_routes_repository, existing_route):
    mock_routes_repository.get_by_flight_id.return_value = [existing_route]
    now = datetime.now(timezone.utc)

    with pytest.raises(RouteAlreadyExistsError):
        await CreateRouteUseCase(mock_routes_repository).execute(
            **create_arguments(now + timedelta(days=1), now + timedelta(days=2))
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("start_offset", "end_offset"),
    [(-2, -1), (2, 1), (1, 1)],
)
async def test_create_route_rejects_invalid_dates(
    mock_routes_repository, start_offset, end_offset
):
    mock_routes_repository.get_by_flight_id.return_value = []
    now = datetime.now(timezone.utc)

    with pytest.raises(InvalidRouteDatesError):
        await CreateRouteUseCase(mock_routes_repository).execute(
            **create_arguments(
                now + timedelta(days=start_offset),
                now + timedelta(days=end_offset),
            )
        )


def test_datetime_helpers_normalize_values():
    aware = datetime(
        2030,
        1,
        1,
        microsecond=123456,
        tzinfo=timezone(timedelta(hours=-5)),
    )
    assert as_utc_naive(aware) == datetime(2030, 1, 1, 5, 0, 0)
    naive = datetime(2030, 1, 1, microsecond=123456)
    assert as_utc_naive(naive) == datetime(2030, 1, 1)
    current = utcnow()
    assert current.tzinfo is None
    assert current.microsecond == 0


@pytest.mark.asyncio
async def test_get_routes_with_and_without_filter(
    mock_routes_repository, existing_route
):
    mock_routes_repository.get_all.return_value = [existing_route]
    mock_routes_repository.get_by_flight_id.return_value = [existing_route]
    use_case = GetRoutesUseCase(mock_routes_repository)

    assert await use_case.execute() == [existing_route]
    assert await use_case.execute("FL-001") == [existing_route]
    mock_routes_repository.get_all.assert_awaited_once()
    mock_routes_repository.get_by_flight_id.assert_awaited_once_with("FL-001")


@pytest.mark.asyncio
async def test_get_route_success_and_not_found(mock_routes_repository, existing_route):
    use_case = GetRouteUseCase(mock_routes_repository)
    mock_routes_repository.get_by_id.return_value = existing_route
    assert await use_case.execute(existing_route.id) == existing_route

    mock_routes_repository.get_by_id.return_value = None
    with pytest.raises(RouteNotFoundError):
        await use_case.execute("missing")


@pytest.mark.asyncio
async def test_delete_route_success_and_not_found(
    mock_routes_repository, existing_route
):
    use_case = DeleteRouteUseCase(mock_routes_repository)
    mock_routes_repository.get_by_id.return_value = existing_route
    await use_case.execute(existing_route.id)
    mock_routes_repository.delete.assert_awaited_once_with(existing_route)

    mock_routes_repository.get_by_id.return_value = None
    with pytest.raises(RouteNotFoundError):
        await use_case.execute("missing")


@pytest.mark.asyncio
async def test_count_and_reset_routes(mock_routes_repository):
    mock_routes_repository.count.return_value = 3
    assert await CountRoutesUseCase(mock_routes_repository).execute() == 3
    await ResetRoutesUseCase(mock_routes_repository).execute()
    mock_routes_repository.delete_all.assert_awaited_once()
