from unittest.mock import MagicMock

from sqlalchemy.ext.asyncio import AsyncSession

from assembly import (
    build_count_routes_use_case,
    build_create_route_use_case,
    build_delete_route_use_case,
    build_get_route_use_case,
    build_get_routes_use_case,
    build_reset_routes_use_case,
    build_routes_repository,
)
from config import Settings
from domain.models.airport_code import Airport_Code, AirportCode


def test_settings_build_database_url(monkeypatch):
    monkeypatch.setenv("DB_HOST", "database")
    monkeypatch.setenv("DB_PORT", "5433")
    monkeypatch.setenv("DB_NAME", "routes")
    monkeypatch.setenv("DB_USER", "app")
    monkeypatch.setenv("DB_PASSWORD", "secret")
    settings = Settings()
    assert settings.app_port == 30002
    assert settings.database_url == (
        "postgresql+asyncpg://app:secret@database:5433/routes"
    )


def test_airport_code_compatibility_alias():
    assert AirportCode.BOG.value == "BOG"
    assert Airport_Code is AirportCode


def test_assembly_builds_repository_and_use_cases():
    session = MagicMock(spec=AsyncSession)
    repository = build_routes_repository(session)
    cases = [
        build_create_route_use_case(repository),
        build_get_routes_use_case(repository),
        build_get_route_use_case(repository),
        build_delete_route_use_case(repository),
        build_count_routes_use_case(repository),
        build_reset_routes_use_case(repository),
    ]
    assert all(case.route_repository is repository for case in cases)
