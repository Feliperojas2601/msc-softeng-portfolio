from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models in routes_app."""


engine = create_async_engine(settings.database_url, future=True)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def init_models() -> None:
    """Create all declared tables when the application starts."""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield one database session for each request."""
    async with async_session_factory() as session:
        yield session
