from unittest.mock import AsyncMock, patch

from entrypoints.api.main import app, lifespan


async def test_lifespan_initializes_the_database_schema():
    """The app's lifespan calls init_models exactly once on startup."""
    with patch(
        "entrypoints.api.main.init_models", new=AsyncMock()
    ) as mocked_init_models:
        async with lifespan(app):
            pass

    mocked_init_models.assert_awaited_once()


def test_app_includes_the_offers_router():
    """The offers router is mounted on the app under the /offers prefix."""
    paths = app.openapi()["paths"]

    assert any(path.startswith("/offers") for path in paths)
