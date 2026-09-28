from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings


class Base(DeclarativeBase):
    """Base class for every SQLAlchemy ORM model in this application."""


engine = create_async_engine(settings.database_url, future=True)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def init_models() -> None:
    """Create every table declared under Base, if it does not exist yet."""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session scoped to a single request."""
    async with async_session_factory() as session:
        yield session
