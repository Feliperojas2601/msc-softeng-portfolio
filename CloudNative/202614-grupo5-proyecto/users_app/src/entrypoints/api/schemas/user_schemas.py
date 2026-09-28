from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from domain.models.user import User, UserStatus

USERNAME_PATTERN = r"^[a-zA-Z0-9_]+$"


class CreateUserRequest(BaseModel):
    """Request body for POST /users."""

    model_config = ConfigDict(populate_by_name=True)

    username: str = Field(pattern=USERNAME_PATTERN)
    password: str = Field(min_length=1)
    email: EmailStr
    dni: str | None = None
    full_name: str | None = Field(default=None, alias="fullName")
    phone_number: str | None = Field(default=None, alias="phoneNumber")


class CreateUserResponse(BaseModel):
    """Response body for POST /users."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    created_at: datetime = Field(alias="createdAt")

    @classmethod
    def from_user(cls, user: User) -> "CreateUserResponse":
        """Build a response from a domain User."""
        return cls(id=user.id, created_at=user.created_at)


class UpdateUserRequest(BaseModel):
    """Request body for PATCH /users/{id}."""

    model_config = ConfigDict(populate_by_name=True)

    status: UserStatus | None = None
    dni: str | None = None
    full_name: str | None = Field(default=None, alias="fullName")
    phone_number: str | None = Field(default=None, alias="phoneNumber")

    @model_validator(mode="after")
    def at_least_one_field_present(self) -> "UpdateUserRequest":
        """Ensure at least one updatable field was sent."""
        if (
            self.status is None
            and self.dni is None
            and self.full_name is None
            and self.phone_number is None
        ):
            raise ValueError("At least one field must be provided")
        return self


class MessageResponse(BaseModel):
    """Generic response body containing only a message."""

    msg: str


class AuthRequest(BaseModel):
    """Request body for POST /users/auth."""

    model_config = ConfigDict(populate_by_name=True)

    username: str
    password: str


class AuthResponse(BaseModel):
    """Response body for POST /users/auth."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    token: str
    expire_at: datetime = Field(alias="expireAt")

    @classmethod
    def from_user(cls, user: User) -> "AuthResponse":
        """Build a response from an authenticated domain User."""
        return cls(id=user.id, token=user.token, expire_at=user.expire_at)


class MeResponse(BaseModel):
    """Response body for GET /users/me."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    username: str
    email: str
    full_name: str | None = Field(default=None, alias="fullName")
    dni: str | None = None
    phone_number: str | None = Field(default=None, alias="phoneNumber")
    status: UserStatus

    @classmethod
    def from_user(cls, user: User) -> "MeResponse":
        """Build a response from a domain User."""
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            dni=user.dni,
            phone_number=user.phone_number,
            status=user.status,
        )


class CountResponse(BaseModel):
    """Response body for GET /users/count."""

    count: int
