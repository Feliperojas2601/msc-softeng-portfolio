import asyncio
import logging
from collections.abc import Callable
from datetime import UTC, datetime

from domain.models.post import (
    CreatedPostResponse,
    CreatedRouteSummary,
    CreatePost,
    CreatePostCommand,
)
from domain.models.route import RouteDetail
from domain.ports.posts_port import PostsPort
from domain.ports.routes_port import RoutesPort
from domain.ports.users_port import UsersPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import (
    DownstreamUnavailableError,
    DuplicatePostError,
    InvalidDatesError,
    InvalidExpirationDateError,
    MissingTokenError,
)

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _find_matching_route(
    routes: list[RouteDetail],
    origin_airport: str,
    origin_country: str,
    destiny_airport: str,
    destiny_country: str,
) -> RouteDetail | None:
    for route in routes:
        if (
            route.source_airport_code == origin_airport
            and route.source_country == origin_country
            and route.destiny_airport_code == destiny_airport
            and route.destiny_country == destiny_country
        ):
            return route
    return None


class CreatePostRf003UseCase(BaseUseCase):

    def __init__(
        self,
        users: UsersPort,
        posts: PostsPort,
        routes: RoutesPort,
        now_provider: Callable[[], datetime] = _utc_now,
    ):
        self.users = users
        self.posts = posts
        self.routes = routes
        self.now_provider = now_provider

    async def execute(self, token: str | None, data: CreatePostCommand) -> CreatePost:
        if not token:
            raise MissingTokenError()

        caller = await self.users.get_me(token)
        now = self.now_provider()

        if (
            data.planned_start_date <= now
            or data.planned_end_date <= data.planned_start_date
        ):
            raise InvalidDatesError("Las fechas del trayecto no son válidas")

        if data.expire_at <= now or data.expire_at > data.planned_start_date:
            raise InvalidExpirationDateError("La fecha expiración no es válida")

        routes = await self.routes.get_routes(flight_id=data.flight_id)

        existing_route = _find_matching_route(
            routes=routes,
            origin_airport=data.origin.airport_code,
            origin_country=data.origin.country,
            destiny_airport=data.destiny.airport_code,
            destiny_country=data.destiny.country,
        )

        route_created_in_this_execution = False

        if existing_route:
            user_posts = await self.posts.get_posts(
                owner=caller.id,
                route=existing_route.id,
            )
            if user_posts:
                raise DuplicatePostError(
                    "El usuario ya tiene una publicación para la misma fecha"
                )
            route = existing_route
        else:
            route = await self.routes.create_route(
                flight_id=data.flight_id,
                source_airport_code=data.origin.airport_code,
                source_country=data.origin.country,
                destiny_airport_code=data.destiny.airport_code,
                destiny_country=data.destiny.country,
                bag_cost=data.bag_cost,
                planned_start_date=data.planned_start_date,
                planned_end_date=data.planned_end_date,
            )
            route_created_in_this_execution = True

        try:
            created_post = await self.posts.create_post(
                user_id=caller.id,
                route_id=str(route.id),
                expire_at=data.expire_at,
            )
        except Exception:
            if route_created_in_this_execution:
                await self._compensate_route(str(route.id))
            raise

        return CreatedPostResponse(
            id=created_post.id,
            user_id=caller.id,
            created_at=created_post.created_at,
            expire_at=data.expire_at,
            route=CreatedRouteSummary(
                id=route.id,
                created_at=route.created_at,
            ),
        )

    async def _compensate_route(self, route_id: str) -> None:
        """Compensación: elimina el trayecto si la creación de la publicación falla."""
        try:
            await self.routes.delete_route(route_id)
            logger.info("Compensación exitosa: ruta %s eliminada.", route_id)
        except DownstreamUnavailableError:
            logger.warning(
                "La compensación falló: la ruta %s no pudo ser eliminada y quedó huérfana.",
                route_id,
            )
        except Exception as e:
            logger.error("Falló la compensación de la ruta %s: %s", route_id, e)
