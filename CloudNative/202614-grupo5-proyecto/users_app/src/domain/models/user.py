from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class UserStatus(str, Enum):
    """Valid lifecycle states of a user."""

    POR_VERIFICAR = "POR_VERIFICAR"
    NO_VERIFICADO = "NO_VERIFICADO"
    VERIFICADO = "VERIFICADO"


class User(BaseModel):
    """User domain model."""

    id: str
    username: str
    email: str
    phone_number: str | None = None
    dni: str | None = None
    full_name: str | None = None
    password: str
    salt: str
    token: str | None = None
    status: UserStatus
    expire_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
