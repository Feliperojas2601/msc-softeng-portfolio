from adapters.database.models import RouteModel
from domain.models.airport_code import AirportCode
from domain.models.route import Route


def route_entity_to_model(route: Route) -> RouteModel:
    """Convert a domain Route into its SQLAlchemy representation."""
    return RouteModel(
        id=route.id,
        flight_id=route.flight_id,
        source_airport_code=route.source_airport_code.value,
        source_country=route.source_country,
        destiny_airport_code=route.destiny_airport_code.value,
        destiny_country=route.destiny_country,
        bag_cost=route.bag_cost,
        planned_start_date=route.planned_start_date,
        planned_end_date=route.planned_end_date,
        created_at=route.created_at,
        updated_at=route.updated_at,
    )


def route_model_to_entity(route_model: RouteModel) -> Route:
    """Convert a SQLAlchemy RouteModel into a domain Route."""
    return Route(
        id=route_model.id,
        flight_id=route_model.flight_id,
        source_airport_code=AirportCode(route_model.source_airport_code),
        source_country=route_model.source_country,
        destiny_airport_code=AirportCode(route_model.destiny_airport_code),
        destiny_country=route_model.destiny_country,
        bag_cost=route_model.bag_cost,
        planned_start_date=route_model.planned_start_date,
        planned_end_date=route_model.planned_end_date,
        created_at=route_model.created_at,
        updated_at=route_model.updated_at,
    )
