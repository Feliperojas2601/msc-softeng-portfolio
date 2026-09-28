from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.database.mappers import route_entity_to_model, route_model_to_entity
from adapters.database.routes_repository_adapter import (
    SQLAlchemyRoutesRepositoryAdapter,
)


def scalar_result(*, all_values=None, one=None, one_or_none=None):
    """Build a small SQLAlchemy result double."""
    scalars = MagicMock()
    scalars.all.return_value = all_values or []
    return SimpleNamespace(
        scalars=lambda: scalars,
        scalar_one=lambda: one,
        scalar_one_or_none=lambda: one_or_none,
    )


def test_route_mapper_round_trip(existing_route):
    model = route_entity_to_model(existing_route)
    restored = route_model_to_entity(model)
    assert restored == existing_route
    assert model.source_airport_code == "BOG"


@pytest.fixture
def session():
    value = MagicMock(spec=AsyncSession)
    value.execute = AsyncMock()
    value.commit = AsyncMock()
    value.refresh = AsyncMock()
    return value


@pytest.mark.asyncio
async def test_repository_create(session, existing_route):
    repository = SQLAlchemyRoutesRepositoryAdapter(session)
    created = await repository.create(existing_route)
    assert created == existing_route
    session.add.assert_called_once()
    session.commit.assert_awaited_once()
    session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_repository_queries(session, existing_route):
    model = route_entity_to_model(existing_route)
    repository = SQLAlchemyRoutesRepositoryAdapter(session)

    session.execute.return_value = scalar_result(all_values=[model])
    assert await repository.get_all() == [existing_route]
    assert await repository.get_by_flight_id("FL-001") == [existing_route]

    session.execute.return_value = scalar_result(one_or_none=model)
    assert await repository.get_by_id(existing_route.id) == existing_route
    session.execute.return_value = scalar_result(one_or_none=None)
    assert await repository.get_by_id("missing") is None


@pytest.mark.asyncio
async def test_repository_count_delete_and_reset(session, existing_route):
    repository = SQLAlchemyRoutesRepositoryAdapter(session)
    session.execute.return_value = scalar_result(one=7)
    assert await repository.count() == 7

    await repository.delete(existing_route)
    await repository.delete_all()
    assert session.commit.await_count == 2
