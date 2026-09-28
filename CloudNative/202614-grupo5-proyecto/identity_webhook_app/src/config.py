from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "identity_webhook_app"
    app_port: int = 30007

    true_native_secret_token: str = "change-me"
    users_app_base_url: str = "http://localhost:30000"
    notifications_app_url: str = "http://localhost:30008"

    http_timeout_seconds: float = 5.0
    http_max_retries: int = 1


settings = Settings()
