from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.database.mappers import route_entity_to_model, route_model_to_entity
from adapters.database.models import RouteModel
from domain.models.route import Route
from domain.ports.routes_repository_port import RoutesRepositoryPort


class SQLAlchemyRoutesRepositoryAdapter(RoutesRepositoryPort):
    """PostgreSQL implementation of RoutesRepositoryPort."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, route: Route) -> Route:
        """Persist a new route."""
        route_model = route_entity_to_model(route)
        self.session.add(route_model)
        await self.session.commit()
        await self.session.refresh(route_model)
        return route_model_to_entity(route_model)

    async def get_by_flight_id(self, flight_id: str) -> list[Route]:
        """Return routes matching a flight identifier."""
        result = await self.session.execute(
            select(RouteModel)
            .where(RouteModel.flight_id == flight_id)
            .order_by(RouteModel.created_at)
        )
        return [route_model_to_entity(model) for model in result.scalars().all()]

    async def get_all(self) -> list[Route]:
        """Return every stored route."""
        result = await self.session.execute(
            select(RouteModel).order_by(RouteModel.created_at)
        )
        return [route_model_to_entity(model) for model in result.scalars().all()]

    async def get_by_id(self, route_id: str) -> Route | None:
        """Return a route by id."""
        result = await self.session.execute(
            select(RouteModel).where(RouteModel.id == route_id)
        )
        model = result.scalar_one_or_none()
        return route_model_to_entity(model) if model else None

    async def delete(self, route: Route) -> None:
        """Delete an existing route."""
        await self.session.execute(delete(RouteModel).where(RouteModel.id == route.id))
        await self.session.commit()

    async def count(self) -> int:
        """Count every stored route."""
        result = await self.session.execute(
            select(func.count()).select_from(RouteModel)
        )
        return result.scalar_one()

    async def delete_all(self) -> None:
        """Delete every stored route."""
        await self.session.execute(delete(RouteModel))
        await self.session.commit()
