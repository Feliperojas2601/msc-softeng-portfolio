from config import Settings


def test_settings_read_downstream_urls_from_env(monkeypatch):
    """Settings pick the downstream URLs up from the environment."""
    monkeypatch.setenv("USERS_APP_URL", "http://users.example")
    monkeypatch.setenv("OFFERS_APP_URL", "http://offers.example")

    settings = Settings()

    assert settings.users_app_url == "http://users.example"
    assert settings.offers_app_url == "http://offers.example"


def test_settings_have_sensible_defaults(monkeypatch):
    """Timeout and retry defaults are applied when nothing overrides them."""
    for var in (
        "HTTP_TIMEOUT_SECONDS",
        "HTTP_MAX_RETRIES",
        "APP_PORT",
    ):
        monkeypatch.delenv(var, raising=False)

    settings = Settings()

    assert settings.app_port == 30005
    assert settings.http_timeout_seconds == 3.0
    assert settings.http_max_retries == 1
