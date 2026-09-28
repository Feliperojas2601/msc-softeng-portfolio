from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "credit_cards_app"
    app_port: int = 30006
    users_app_url: str = "http://users-app-service"
    users_timeout_seconds: float = Field(default=2.0, gt=0)
    true_native_base_url: str = "http://true-native-service"
    true_native_secret_token: str = "change-me"
    true_native_timeout_seconds: float = Field(default=2.0, gt=0)
    credit_cards_internal_secret: str = ""
    db_host: str = "credit_cards_db"
    db_port: int = 5432
    db_name: str = "credit_cards_db"
    db_user: str = "credit_cards_app"
    db_password: str = "postgres"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
