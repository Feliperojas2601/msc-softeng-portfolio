from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import PlainTextResponse

from assembly import (
    build_count_routes_use_case,
    build_create_route_use_case,
    build_delete_route_use_case,
    build_get_route_use_case,
    build_get_routes_use_case,
    build_reset_routes_use_case,
)
from domain.use_cases.count_routes_use_case import CountRoutesUseCase
from domain.use_cases.create_route_use_case import CreateRouteUseCase
from domain.use_cases.delete_route_use_case import DeleteRouteUseCase
from domain.use_cases.get_route_use_case import GetRouteUseCase
from domain.use_cases.get_routes_use_case import GetRoutesUseCase
from domain.use_cases.reset_routes_use_case import ResetRoutesUseCase
from entrypoints.api.schemas.route_schemas import (
    CountResponse,
    CreateRouteRequest,
    CreateRouteResponse,
    MessageResponse,
    RouteResponse,
)

router = APIRouter(prefix="/routes")


@router.post(
    "", response_model=CreateRouteResponse, status_code=status.HTTP_201_CREATED
)
async def create_route(
    body: CreateRouteRequest,
    use_case: CreateRouteUseCase = Depends(build_create_route_use_case),
) -> CreateRouteResponse:
    """Create a route with a unique flight identifier."""
    route = await use_case.execute(
        flight_id=body.flightId,
        source_airport_code=body.sourceAirportCode,
        source_country=body.sourceCountry,
        destiny_airport_code=body.destinyAirportCode,
        destiny_country=body.destinyCountry,
        bag_cost=body.bagCost,
        planned_start_date=body.plannedStartDate,
        planned_end_date=body.plannedEndDate,
    )
    return CreateRouteResponse.from_route(route)


@router.get("", response_model=list[RouteResponse])
async def get_routes(
    flight_id: str | None = Query(default=None, alias="flight", min_length=1),
    use_case: GetRoutesUseCase = Depends(build_get_routes_use_case),
) -> list[RouteResponse]:
    """List every route or filter by flight id."""
    routes = await use_case.execute(flight_id)
    return [RouteResponse.from_route(route) for route in routes]


@router.get("/count", response_model=CountResponse)
async def count_routes(
    use_case: CountRoutesUseCase = Depends(build_count_routes_use_case),
) -> CountResponse:
    """Return the number of stored routes."""
    return CountResponse(count=await use_case.execute())


@router.get("/ping", response_class=PlainTextResponse)
async def ping() -> str:
    """Healthcheck endpoint."""
    return "pong"


@router.post("/reset", response_model=MessageResponse)
async def reset_routes(
    use_case: ResetRoutesUseCase = Depends(build_reset_routes_use_case),
) -> MessageResponse:
    """Delete every stored route."""
    await use_case.execute()
    return MessageResponse(msg="Todos los datos fueron eliminados")


@router.get("/{route_id}", response_model=RouteResponse)
async def get_route(
    route_id: UUID,
    use_case: GetRouteUseCase = Depends(build_get_route_use_case),
) -> RouteResponse:
    """Return a route by id."""
    route = await use_case.execute(str(route_id))
    return RouteResponse.from_route(route)


@router.delete("/{route_id}", response_model=MessageResponse)
async def delete_route(
    route_id: UUID,
    use_case: DeleteRouteUseCase = Depends(build_delete_route_use_case),
) -> MessageResponse:
    """Delete a route by id."""
    await use_case.execute(str(route_id))
    return MessageResponse(msg="el trayecto fue eliminado")
