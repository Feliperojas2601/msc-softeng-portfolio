from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.database.mappers import user_entity_to_model
from adapters.database.user_repository_adapter import SQLAlchemyUserRepositoryAdapter


def _execute_result(scalar_value):
    result = MagicMock()
    result.scalar_one_or_none.return_value = scalar_value
    result.scalar_one.return_value = scalar_value
    return result


@pytest.fixture
def mock_session():
    """Fixture providing a fully mocked SQLAlchemy AsyncSession, respecting its sync/async API."""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def adapter(mock_session):
    """Fixture providing a SQLAlchemyUserRepositoryAdapter bound to a mocked session."""
    return SQLAlchemyUserRepositoryAdapter(mock_session)


async def test_create_adds_and_commits(adapter, mock_session, existing_user):
    """create() adds the model to the session and commits."""
    created = await adapter.create(existing_user)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    assert created.id == existing_user.id


async def test_get_by_id_returns_none_when_missing(adapter, mock_session):
    """get_by_id returns None when no row matches."""
    mock_session.execute.return_value = _execute_result(None)

    assert await adapter.get_by_id("missing") is None


async def test_get_by_username_returns_entity_when_found(
    adapter, mock_session, existing_user
):
    """get_by_username maps the found row back to a domain User."""
    model = user_entity_to_model(existing_user)
    mock_session.execute.return_value = _execute_result(model)

    result = await adapter.get_by_username(existing_user.username)

    assert result.username == existing_user.username


async def test_get_by_email_returns_entity_when_found(
    adapter, mock_session, existing_user
):
    """get_by_email maps the found row back to a domain User."""
    model = user_entity_to_model(existing_user)
    mock_session.execute.return_value = _execute_result(model)

    result = await adapter.get_by_email(existing_user.email)

    assert result.email == existing_user.email


async def test_get_by_token_returns_entity_when_found(
    adapter, mock_session, existing_user
):
    """get_by_token maps the found row back to a domain User."""
    existing_user.token = "some-token"
    model = user_entity_to_model(existing_user)
    mock_session.execute.return_value = _execute_result(model)

    result = await adapter.get_by_token("some-token")

    assert result.token == "some-token"


async def test_update_persists_changes_and_returns_entity(
    adapter, mock_session, existing_user
):
    """update() copies every field from the domain user onto the ORM row."""
    model = user_entity_to_model(existing_user)
    mock_session.execute.return_value = _execute_result(model)

    existing_user.full_name = "Updated Name"
    result = await adapter.update(existing_user)

    assert model.full_name == "Updated Name"
    assert result.full_name == "Updated Name"
    mock_session.commit.assert_awaited_once()


async def test_count_returns_scalar_value(adapter, mock_session):
    """count() returns whatever the query's scalar result is."""
    mock_session.execute.return_value = _execute_result(7)

    assert await adapter.count() == 7


async def test_delete_all_executes_delete_and_commits(adapter, mock_session):
    """delete_all() issues a delete statement and commits it."""
    mock_session.execute.return_value = MagicMock()

    await adapter.delete_all()

    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
