from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

from adapters.database import session as session_module


async def test_init_models_creates_the_schema_on_the_engine():
    """init_models opens a connection and runs create_all against it."""
    connection = AsyncMock()

    @asynccontextmanager
    async def fake_begin():
        yield connection

    fake_engine = MagicMock()
    fake_engine.begin = fake_begin

    with patch.object(session_module, "engine", fake_engine):
        await session_module.init_models()

    connection.run_sync.assert_awaited_once_with(
        session_module.Base.metadata.create_all
    )


async def test_get_session_yields_a_session_from_the_factory():
    """get_session yields exactly one session obtained from the session factory."""
    fake_session = MagicMock()

    @asynccontextmanager
    async def fake_session_factory():
        yield fake_session

    with patch.object(session_module, "async_session_factory", fake_session_factory):
        sessions = [item async for item in session_module.get_session()]

    assert sessions == [fake_session]
