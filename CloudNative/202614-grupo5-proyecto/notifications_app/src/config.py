from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
    AWS_SESSION_TOKEN) are read directly by boto3 from the environment via
    its default credential chain; they are not declared here.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "notifications_app"
    app_port: int = 30008

    aws_region: str = "us-east-1"
    sns_topic_arn: str = "arn:aws:sns:us-east-1:000000000000:change-me"


settings = Settings()
