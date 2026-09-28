from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "posts_app"
    app_port: int = 30000

    db_host: str = "posts_db"
    db_port: int = 5432
    db_name: str = "posts_db"
    db_user: str = "posts_app"
    db_password: str = "postgres"

    token_expiration_hours: int = 24

    @property
    def database_url(self) -> str:
        """Build the async SQLAlchemy connection URL for PostgreSQL."""
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
