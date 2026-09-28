from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from assembly import (
    build_count_posts_use_case,
    build_create_post_use_case,
    build_delete_post_use_case,
    build_get_post_by_id_use_case,
    build_get_post_filter_use_case,
    build_reset_posts_use_case,
)
from entrypoints.api.main import app
from errors import ExpirationDateNoValid, PostNotFoundError


@pytest.fixture
def client():
    """Fixture providing a TestClient that never runs the app's lifespan (no real DB)."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_overrides():
    """Ensure dependency overrides never leak between tests."""
    yield
    app.dependency_overrides.clear()


def _override(builder, use_case):
    app.dependency_overrides[builder] = lambda: use_case


def test_create_post_success(client, existing_post):
    """POST /posts returns 201 with id, userId, and createdAt on success."""
    use_case = AsyncMock()
    use_case.execute.return_value = existing_post
    _override(build_create_post_use_case, use_case)

    future_date = (datetime.now(UTC) + timedelta(days=7)).isoformat()
    response = client.post(
        "/posts/",
        json={
            "routeId": "a1b2c3d4-1111-4000-8000-000000000001",
            "userId": "b2c3d4e5-2222-4000-8000-000000000002",
            "expireAt": future_date,
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == existing_post.id
    assert body["userId"] == existing_post.userId
    assert "createdAt" in body


def test_create_post_invalid_fields_returns_400(client):
    """POST /posts returns 400 when required fields are missing or invalid."""
    response = client.post(
        "/posts/",
        json={
            "routeId": "invalid-uuid",
        },
    )
    assert response.status_code == 400


def test_create_post_invalid_expiration_date_returns_412(client):
    """POST /posts returns 412 when expiration date is not in the future."""
    use_case = AsyncMock()
    use_case.execute.side_effect = ExpirationDateNoValid(
        "La fecha expiración no es válida"
    )
    _override(build_create_post_use_case, use_case)

    past_date = (datetime.now(UTC) - timedelta(days=1)).isoformat()
    response = client.post(
        "/posts/",
        json={
            "routeId": "a1b2c3d4-1111-4000-8000-000000000001",
            "userId": "b2c3d4e5-2222-4000-8000-000000000002",
            "expireAt": past_date,
        },
    )

    assert response.status_code == 412
    assert response.json()["msg"] == "La fecha expiración no es válida"


def test_get_all_posts_without_filters(client, existing_post, existing_post_2):
    """GET /posts returns all posts when no query parameters are passed."""
    use_case = AsyncMock()
    use_case.execute.return_value = [existing_post, existing_post_2]
    _override(build_get_post_filter_use_case, use_case)

    response = client.get("/posts/")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert body[0]["id"] == existing_post.id
    assert body[1]["id"] == existing_post_2.id


def test_get_all_posts_with_query_filters(client, existing_post):
    """GET /posts applies query filters and returns matching records."""
    use_case = AsyncMock()
    use_case.execute.return_value = [existing_post]
    _override(build_get_post_filter_use_case, use_case)

    response = client.get(
        f"/posts/?expire=false&route={existing_post.routeId}&owner={existing_post.userId}"
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == existing_post.id
    use_case.execute.assert_awaited_once()


def test_get_all_posts_invalid_query_returns_400(client):
    """GET /posts returns 400 when query parameter types are invalid."""
    response = client.get("/posts/?expire=not-a-boolean")
    assert response.status_code == 400


def test_get_post_by_id_success(client, existing_post):
    """GET /posts/{id} returns post object when found."""
    use_case = AsyncMock()
    use_case.execute.return_value = existing_post
    _override(build_get_post_by_id_use_case, use_case)

    response = client.get(f"/posts/{existing_post.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == existing_post.id
    assert body["routeId"] == existing_post.routeId
    assert body["userId"] == existing_post.userId


def test_get_post_by_id_invalid_uuid_returns_400(client):
    """GET /posts/{id} returns 400 if id path parameter is not a valid UUID."""
    response = client.get("/posts/not-a-valid-uuid")
    assert response.status_code == 400


def test_get_post_by_id_not_found_returns_404(client):
    """GET /posts/{id} returns 404 when post does not exist."""
    use_case = AsyncMock()
    use_case.execute.side_effect = PostNotFoundError("Publicación no encontrada")
    _override(build_get_post_by_id_use_case, use_case)

    response = client.get("/posts/a1b2c3d4-1111-4000-8000-000000000099")
    assert response.status_code == 404


def test_delete_post_success(client, existing_post):
    """DELETE /posts/{id} removes post and returns confirmation message."""
    use_case = AsyncMock()
    use_case.execute.return_value = None
    _override(build_delete_post_use_case, use_case)

    response = client.delete(f"/posts/{existing_post.id}")

    assert response.status_code == 200
    assert response.json() == {"msg": "la publicación fue eliminada"}


def test_delete_post_invalid_uuid_returns_400(client):
    """DELETE /posts/{id} returns 400 when id is not a valid UUID."""
    response = client.delete("/posts/invalid-uuid-format")
    assert response.status_code == 400


def test_delete_post_not_found_returns_404(client):
    """DELETE /posts/{id} returns 404 when target post does not exist."""
    use_case = AsyncMock()
    use_case.execute.side_effect = PostNotFoundError("Publicación no encontrada")
    _override(build_delete_post_use_case, use_case)

    response = client.delete("/posts/a1b2c3d4-1111-4000-8000-000000000099")
    assert response.status_code == 404


def test_count_posts_success(client):
    """GET /posts/count returns total integer count."""
    use_case = AsyncMock()
    use_case.execute.return_value = 5
    _override(build_count_posts_use_case, use_case)

    response = client.get("/posts/count")

    assert response.status_code == 200
    assert response.json() == {"count": 5}


def test_ping_success(client):
    """GET /posts/ping returns plain text 'pong'."""
    response = client.get("/posts/ping")

    assert response.status_code == 200
    assert response.text == "pong"


def test_reset_posts_success(client):
    """POST /posts/reset wipes all posts and returns confirmation message."""
    use_case = AsyncMock()
    use_case.execute.return_value = None
    _override(build_reset_posts_use_case, use_case)

    response = client.post("/posts/reset")

    assert response.status_code == 200
    assert response.json() == {"msg": "Todos los datos fueron eliminados"}
