from entrypoints.api.main import app


def test_app_includes_the_verification_and_health_routers():
    """The verify-callback and ping routes are mounted on the app."""
    paths = app.openapi()["paths"]

    assert "/verify-callback" in paths
    assert "/ping" in paths
