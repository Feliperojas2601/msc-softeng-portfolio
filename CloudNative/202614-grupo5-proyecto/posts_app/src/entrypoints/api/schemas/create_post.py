from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from domain.models.post import Post


class CreatePost(BaseModel):
    """Request body for POST /posts."""

    model_config = ConfigDict(populate_by_name=True)

    routeId: UUID = Field(..., description="ID del trayecto en formato UUID")
    userId: UUID = Field(..., description="ID del usuario en formato UUID")
    expireAt: datetime


class CreatePostResponse(BaseModel):
    """Response body for POST /posts."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    user_id: str = Field(alias="userId")
    created_at: datetime = Field(alias="createdAt")

    @classmethod
    def from_post(cls, post: Post) -> "CreatePostResponse":
        """Build a response from a domain Post."""
        return cls(
            id=post.id,
            user_id=post.userId,
            created_at=post.createdAt,
        )
