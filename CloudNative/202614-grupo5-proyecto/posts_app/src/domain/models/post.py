from datetime import datetime

from pydantic import BaseModel, Field


class Post(BaseModel):
    """Post domain model."""

    id: str = Field(
        min_length=1, description="Identificador de publicación en formato UUID"
    )
    routeId: str = Field(min_length=1, description="Identificador de Ruta")
    userId: str = Field(min_length=1, description="Identificador de Usuario")
    expireAt: datetime
    createdAt: datetime
