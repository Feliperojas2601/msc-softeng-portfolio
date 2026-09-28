from pydantic import BaseModel, Field


class Caller(BaseModel):
    """Usuario autenticado que realiza solicitudes."""

    id: str = Field(min_length=1, description="Identificador del usuario autenticado")
    status: str | None = Field(
        default=None, description="Estado del usuario reportado por users_app"
    )
