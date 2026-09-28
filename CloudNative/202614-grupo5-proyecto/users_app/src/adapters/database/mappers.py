from adapters.database.models import UserModel
from domain.models.user import User, UserStatus


def user_entity_to_model(user: User) -> UserModel:
    """Convert a domain User into its SQLAlchemy ORM representation."""
    return UserModel(
        id=user.id,
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        dni=user.dni,
        full_name=user.full_name,
        password=user.password,
        salt=user.salt,
        token=user.token,
        status=user.status.value,
        expire_at=user.expire_at,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def user_model_to_entity(user_model: UserModel) -> User:
    """Convert a SQLAlchemy ORM user into its domain representation."""
    return User(
        id=user_model.id,
        username=user_model.username,
        email=user_model.email,
        phone_number=user_model.phone_number,
        dni=user_model.dni,
        full_name=user_model.full_name,
        password=user_model.password,
        salt=user_model.salt,
        token=user_model.token,
        status=UserStatus(user_model.status),
        expire_at=user_model.expire_at,
        created_at=user_model.created_at,
        updated_at=user_model.updated_at,
    )
