from config import Settings


def test_database_url_builds_asyncpg_connection_string():
    """database_url assembles a valid asyncpg SQLAlchemy connection string."""
    settings = Settings(
        db_user="user",
        db_password="pwd",  # nosec B106
        db_host="db-host",
        db_port=5432,
        db_name="mydb",
    )

    assert settings.database_url == "postgresql+asyncpg://user:pwd@db-host:5432/mydb"
