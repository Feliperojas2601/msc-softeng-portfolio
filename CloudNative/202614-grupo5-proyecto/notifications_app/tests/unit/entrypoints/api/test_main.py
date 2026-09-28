from entrypoints.api.main import app


def test_app_includes_the_notify_and_health_routers():
    """The notify and ping routes are mounted on the app."""
    paths = app.openapi()["paths"]

    assert "/notify" in paths
    assert "/ping" in paths
