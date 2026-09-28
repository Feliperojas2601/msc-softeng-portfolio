from datetime import UTC, datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from domain.models.caller import Caller
from domain.models.post import (
    CreatedPostResponse,
    CreatePost,
    CreatePostCommand,
    Location,
)
from domain.models.route import CreatedRoute, RouteDetail
from domain.use_cases.create_post_rf003_use_case import CreatePostRf003UseCase
from errors import (
    DownstreamUnavailableError,
    DuplicatePostError,
    InvalidDatesError,
    InvalidExpirationDateError,
    InvalidTokenError,
    MissingTokenError,
)


@pytest.fixture
def fixed_now():
    """Hora actual congelada para evaluar correctamente las fechas."""
    return lambda: datetime(2026, 1, 1, 10, 0, 0, tzinfo=UTC)


@pytest.fixture
def caller_user():
    """Usuario simulado devuelto por users_port."""
    return Caller(id="user-123")


@pytest.fixture
def command():
    return CreatePostCommand(
        flight_id="AV123",
        expire_at=datetime(2026, 5, 9, 23, 59, 0, tzinfo=timezone.utc),
        planned_start_date=datetime(2026, 5, 10, 8, 0, 0, tzinfo=timezone.utc),
        planned_end_date=datetime(2026, 5, 10, 16, 0, 0, tzinfo=timezone.utc),
        origin=Location(airport_code="BOG", country="CO"),
        destiny=Location(airport_code="MIA", country="US"),
        bag_cost=25.50,
    )


@pytest.fixture
def existing_route_detail():
    """Ruta devuelta por routes_port.get_routes cuando ya coincide en origen y destino."""
    return RouteDetail(
        id="route-existing-1",
        flight_id="AV123",
        source_airport_code="BOG",
        source_country="CO",
        destiny_airport_code="MIA",
        destiny_country="US",
        bag_cost=25.0,
        created_at=datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC),
    )


@pytest.fixture
def created_route_obj():
    """Respuesta devuelta cuando routes_port.create_route crea un nuevo trayecto."""
    return CreatedRoute(
        id="route-new-1",
        created_at=datetime(2026, 1, 1, 11, 0, 0, tzinfo=UTC),
    )


@pytest.fixture
def created_post_obj():
    """Respuesta devuelta por posts_port.create_post."""
    return CreatePost(
        id="post-999",
        user_id="user-123",
        created_at=datetime(2026, 1, 1, 11, 30, 0, tzinfo=UTC),
    )


@pytest.fixture
def users_port(caller_user):
    port = MagicMock()
    port.get_me = AsyncMock(return_value=caller_user)
    return port


@pytest.fixture
def posts_port(created_post_obj):
    port = MagicMock()
    port.get_posts = AsyncMock(return_value=[])
    port.create_post = AsyncMock(return_value=created_post_obj)
    return port


@pytest.fixture
def routes_port(created_route_obj):
    port = MagicMock()
    port.get_routes = AsyncMock(return_value=[])
    port.create_route = AsyncMock(return_value=created_route_obj)
    port.delete_route = AsyncMock()
    return port


@pytest.fixture
def use_case(users_port, posts_port, routes_port, fixed_now):
    """Caso de uso configurado con los puertos e inyección de reloj simulado."""
    return CreatePostRf003UseCase(
        users=users_port,
        posts=posts_port,
        routes=routes_port,
        now_provider=fixed_now,
    )


async def test_happy_path_with_new_route_creation(
    use_case,
    users_port,
    posts_port,
    routes_port,
    command,
    created_route_obj,
    created_post_obj,
):
    """Si no existe la ruta, se crea una nueva y finaliza la creación de la publicación."""
    routes_port.get_routes.return_value = []

    result = await use_case.execute("valid-token", command)

    users_port.get_me.assert_awaited_once_with("valid-token")
    routes_port.get_routes.assert_awaited_once_with(flight_id="AV123")
    routes_port.create_route.assert_awaited_once_with(
        flight_id="AV123",
        source_airport_code="BOG",
        source_country="CO",
        destiny_airport_code="MIA",
        destiny_country="US",
        bag_cost=25.5,
        planned_start_date=command.planned_start_date,
        planned_end_date=command.planned_end_date,
    )
    posts_port.get_posts.assert_not_awaited()
    posts_port.create_post.assert_awaited_once_with(
        user_id="user-123",
        route_id="route-new-1",
        expire_at=command.expire_at,
    )

    assert isinstance(result, CreatedPostResponse)
    assert result.id == "post-999"
    assert result.user_id == "user-123"
    assert result.route.id == "route-new-1"


async def test_happy_path_reusing_existing_route(
    use_case, posts_port, routes_port, command, existing_route_detail
):
    """Si la ruta ya existe, se reutiliza y NO se llama a create_route."""
    routes_port.get_routes.return_value = [existing_route_detail]

    result = await use_case.execute("valid-token", command)

    routes_port.create_route.assert_not_awaited()
    posts_port.get_posts.assert_awaited_once_with(
        owner="user-123", route="route-existing-1"
    )
    posts_port.create_post.assert_awaited_once_with(
        user_id="user-123",
        route_id="route-existing-1",
        expire_at=command.expire_at,
    )
    assert result.route.id == "route-existing-1"


async def test_missing_token_raises_error_before_downstream_calls(
    use_case, users_port, command
):
    """Sin token falla directamente con MissingTokenError y no invoca a users_app."""
    with pytest.raises(MissingTokenError):
        await use_case.execute(None, command)

    users_port.get_me.assert_not_awaited()


async def test_invalid_token_propagates(use_case, users_port, command):
    """Token inválido propaga InvalidTokenError al llamar a get_me."""
    users_port.get_me.side_effect = InvalidTokenError()

    with pytest.raises(InvalidTokenError):
        await use_case.execute("bad-token", command)


@pytest.mark.parametrize(
    "start, end",
    [
        (
            datetime(2025, 12, 31, tzinfo=UTC),
            datetime(2026, 5, 10, tzinfo=UTC),
        ),
        (datetime(2026, 5, 10, tzinfo=UTC), datetime(2026, 5, 10, tzinfo=UTC)),
        (datetime(2026, 5, 10, tzinfo=UTC), datetime(2026, 5, 9, tzinfo=UTC)),
    ],
)
async def test_invalid_dates_raises_error(use_case, command, start, end):
    """Fechas del trayecto no válidas arrojan InvalidDatesError."""
    invalid_command = command.model_copy(
        update={"planned_start_date": start, "planned_end_date": end}
    )

    with pytest.raises(InvalidDatesError):
        await use_case.execute("valid-token", invalid_command)


@pytest.mark.parametrize(
    "expire_at",
    [
        datetime(2025, 12, 31, tzinfo=UTC),
        datetime(2026, 5, 11, tzinfo=UTC),
    ],
)
async def test_invalid_expiration_date_raises_error(use_case, command, expire_at):
    """Fecha de expiración inválida o extemporánea arroja InvalidExpirationDateError."""
    invalid_command = command.model_copy(update={"expire_at": expire_at})

    with pytest.raises(InvalidExpirationDateError):
        await use_case.execute("valid-token", invalid_command)


async def test_duplicate_post_raises_error_without_compensation_if_route_existed(
    use_case, posts_port, routes_port, command, existing_route_detail
):
    """Si la ruta existía y el usuario ya tenía un post en esa ruta, lanza DuplicatePostError sin llamar a compensación."""
    routes_port.get_routes.return_value = [existing_route_detail]

    existing_post = MagicMock()
    posts_port.get_posts.return_value = [existing_post]

    with pytest.raises(DuplicatePostError):
        await use_case.execute("valid-token", command)

    routes_port.delete_route.assert_not_awaited()


async def test_create_post_failure_compensates_created_route(
    use_case, posts_port, routes_port, command
):
    """Si falla posts_port.create_post con DownstreamUnavailableError, se ejecuta la compensación de la ruta creada."""
    posts_port.create_post.side_effect = DownstreamUnavailableError()

    with pytest.raises(DownstreamUnavailableError):
        await use_case.execute("valid-token", command)

    routes_port.delete_route.assert_awaited_once_with("route-new-1")


async def test_compensation_failure_is_swallowed_and_original_error_raised(
    use_case, posts_port, routes_port, command
):
    """Si la compensación falla (delete_route lanza excepción), el error de compensación es silenciado por el logger y se propaga el error original."""
    posts_port.create_post.side_effect = DownstreamUnavailableError()
    routes_port.delete_route.side_effect = DownstreamUnavailableError()

    with pytest.raises(DownstreamUnavailableError):
        await use_case.execute("valid-token", command)

    routes_port.delete_route.assert_awaited_once_with("route-new-1")
