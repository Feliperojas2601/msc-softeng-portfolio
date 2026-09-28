from adapters.database.post_model import PostModel
from domain.models.post import Post


def post_entity_to_model(post: Post) -> PostModel:
    """Map Post domain entity to SQLAlchemy PostModel."""
    return PostModel(
        id=post.id,
        route_id=post.routeId,
        user_id=post.userId,
        expire_at=post.expireAt,
        created_at=post.createdAt,
    )


def post_model_to_entity(model: PostModel) -> Post:
    """Map SQLAlchemy PostModel to Post domain entity."""
    return Post(
        id=model.id,
        routeId=model.route_id,
        userId=model.user_id,
        expireAt=model.expire_at,
        createdAt=model.created_at,
    )
