from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "routes_app"
    app_port: int = 30002

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "routes_db"
    db_user: str = "postgres"
    db_password: str = "postgres"

    @property
    def database_url(self) -> str:
        """Build the async SQLAlchemy connection URL for PostgreSQL."""
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
