from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.database.mappers import user_entity_to_model, user_model_to_entity
from adapters.database.models import UserModel
from domain.models.user import User
from domain.ports.user_repository_port import UserRepositoryPort


class SQLAlchemyUserRepositoryAdapter(UserRepositoryPort):
    """PostgreSQL implementation of UserRepositoryPort using SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        """Persist a new user."""
        user_model = user_entity_to_model(user)
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
        return user_model_to_entity(user_model)

    async def get_by_id(self, user_id: str) -> User | None:
        """Fetch a user by its id."""
        return await self._get_by(UserModel.id, user_id)

    async def get_by_username(self, username: str) -> User | None:
        """Fetch a user by its username."""
        return await self._get_by(UserModel.username, username)

    async def get_by_email(self, email: str) -> User | None:
        """Fetch a user by its email."""
        return await self._get_by(UserModel.email, email)

    async def get_by_token(self, token: str) -> User | None:
        """Fetch a user by its current session token."""
        return await self._get_by(UserModel.token, token)

    async def update(self, user: User) -> User:
        """Persist changes made to an existing user."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        user_model = result.scalar_one()

        user_model.username = user.username
        user_model.email = user.email
        user_model.phone_number = user.phone_number
        user_model.dni = user.dni
        user_model.full_name = user.full_name
        user_model.password = user.password
        user_model.salt = user.salt
        user_model.token = user.token
        user_model.status = user.status.value
        user_model.expire_at = user.expire_at
        user_model.updated_at = user.updated_at

        await self.session.commit()
        await self.session.refresh(user_model)
        return user_model_to_entity(user_model)

    async def count(self) -> int:
        """Count how many users exist."""
        result = await self.session.execute(select(func.count()).select_from(UserModel))
        return result.scalar_one()

    async def delete_all(self) -> None:
        """Delete every user, used to reset the database."""
        await self.session.execute(delete(UserModel))
        await self.session.commit()

    async def _get_by(self, column, value: str) -> User | None:
        result = await self.session.execute(select(UserModel).where(column == value))
        user_model = result.scalar_one_or_none()
        return user_model_to_entity(user_model) if user_model else None
