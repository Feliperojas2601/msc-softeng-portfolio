from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación cargada desde variables de entorno."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "orchestrator_app"
    app_port: int = 30005

    users_app_url: str = "http://localhost:30000"
    posts_app_url: str = "http://localhost:30001"
    routes_app_url: str = "http://localhost:30002"
    offers_app_url: str = "http://localhost:30003"
    scores_app_url: str = "http://localhost:30004"

    http_timeout_seconds: float = 3.0
    http_max_retries: int = 1


settings = Settings()
