from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from domain.models.post import Post


class PostResponse(BaseModel):
    """Response body for GET /posts/{id} and items in GET /posts list."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    route_id: str = Field(alias="routeId")
    user_id: str = Field(alias="userId")
    expire_at: datetime = Field(alias="expireAt")
    created_at: datetime = Field(alias="createdAt")

    @classmethod
    def from_post(cls, post: Post) -> "PostResponse":
        """Build a response from a domain Post."""
        return cls(
            id=post.id,
            route_id=post.routeId,
            user_id=post.userId,
            expire_at=post.expireAt,
            created_at=post.createdAt,
        )


class MessageResponse(BaseModel):
    """Generic response body containing only a message."""

    msg: str


class CountResponse(BaseModel):
    """Response body for GET /posts/count."""

    count: int
