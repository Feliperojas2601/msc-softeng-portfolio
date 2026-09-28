import json
from datetime import UTC, datetime

import httpx
import pytest
import respx

from adapters.http.posts_adapter import HttpPostsAdapter
from errors import DownstreamUnavailableError, PostNotFoundError

BASE = "http://posts.test"


@pytest.fixture
def adapter() -> HttpPostsAdapter:
    """Un adaptador de publicaciones con un intento de reintento configurado."""
    return HttpPostsAdapter(BASE, timeout=1.0, max_retries=1)


@respx.mock
async def test_get_post_projects_response(adapter: HttpPostsAdapter):
    """Una respuesta 200 se proyecta a un Post normalizando las fechas a UTC."""
    respx.get(f"{BASE}/posts/post-1").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "post-1",
                "routeId": "route-1",
                "userId": "user-2",
                "expireAt": "2026-12-31T23:59:59",
                "createdAt": "2026-01-01T00:00:00",
            },
        )
    )

    post = await adapter.get_post("post-1")

    assert post.id == "post-1"
    assert post.route_id == "route-1"
    assert post.user_id == "user-2"
    assert post.expire_at.tzinfo is not None
    assert post.expire_at.astimezone(UTC).year == 2026


@respx.mock
async def test_get_post_maps_404_to_not_found(adapter: HttpPostsAdapter):
    """Un status 404 lanza PostNotFoundError."""
    respx.get(f"{BASE}/posts/ghost").mock(return_value=httpx.Response(404))

    with pytest.raises(PostNotFoundError):
        await adapter.get_post("ghost")


@respx.mock
async def test_get_post_maps_5xx_to_downstream_unavailable(adapter: HttpPostsAdapter):
    """Un status 503 lanza DownstreamUnavailableError."""
    respx.get(f"{BASE}/posts/post-1").mock(return_value=httpx.Response(503))

    with pytest.raises(DownstreamUnavailableError):
        await adapter.get_post("post-1")


@respx.mock
async def test_create_post_success(adapter: HttpPostsAdapter):
    """Petición POST /posts exitosa retorna CreatePost instanciado."""
    expire_at = datetime(2026, 12, 31, 23, 59, 59, tzinfo=UTC)

    route = respx.post(f"{BASE}/posts").mock(
        return_value=httpx.Response(
            201,
            json={
                "id": "post-100",
                "userId": "user-1",
                "createdAt": "2026-01-01T10:00:00Z",
            },
        )
    )

    result = await adapter.create_post(
        user_id="user-1",
        route_id="route-50",
        expire_at=expire_at,
    )

    assert route.called
    sent_payload = json.loads(route.calls.last.request.content)

    assert sent_payload["routeId"] == "route-50"
    assert sent_payload["userId"] == "user-1"
    assert "2026-12-31" in sent_payload["expireAt"]

    assert result.id == "post-100"


@respx.mock
async def test_create_post_maps_error_to_downstream_unavailable(
    adapter: HttpPostsAdapter,
):
    """Si la creación retorna un código de error (ej. 500), se lanza DownstreamUnavailableError."""
    respx.post(f"{BASE}/posts").mock(return_value=httpx.Response(500))

    with pytest.raises(DownstreamUnavailableError):
        await adapter.create_post(
            user_id="user-1",
            route_id="route-50",
            expire_at=datetime.now(UTC),
        )


@respx.mock
async def test_get_posts_with_filters(adapter: HttpPostsAdapter):
    """GET /posts envía adecuadamente los query params y retorna la lista de Post."""
    route = respx.get(f"{BASE}/posts").mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "id": "post-1",
                    "routeId": "route-10",
                    "userId": "user-1",
                    "expireAt": "2026-12-31T23:59:59Z",
                    "createdAt": "2026-01-01T00:00:00Z",
                }
            ],
        )
    )

    posts = await adapter.get_posts(expire=False, route="route-10", owner="user-1")

    assert route.called
    query_params = route.calls.last.request.url.query.decode()
    assert "expire=false" in query_params
    assert "route=route-10" in query_params
    assert "owner=user-1" in query_params

    assert len(posts) == 1
    assert posts[0].id == "post-1"


@respx.mock
async def test_get_posts_maps_5xx_to_downstream_unavailable(adapter: HttpPostsAdapter):
    """Un error 500 en GET /posts lanza DownstreamUnavailableError."""
    respx.get(f"{BASE}/posts").mock(return_value=httpx.Response(500))

    with pytest.raises(DownstreamUnavailableError):
        await adapter.get_posts(route="route-10")
