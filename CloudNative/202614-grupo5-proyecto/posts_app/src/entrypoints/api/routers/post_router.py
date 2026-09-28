from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.responses import PlainTextResponse

from assembly import (
    build_count_posts_use_case,
    build_create_post_use_case,
    build_delete_post_use_case,
    build_get_post_by_id_use_case,
    build_get_post_filter_use_case,
    build_reset_posts_use_case,
)
from domain.use_cases.base_use_case import BaseUseCase
from domain.use_cases.count_posts_use_case import CountPostsUseCase
from domain.use_cases.delete_post_use_case import DeletePostUseCase
from domain.use_cases.get_post_filter_use_case import GetPostFiltersUseCase
from domain.use_cases.get_post_use_case import GetPostUseCase
from domain.use_cases.reset_posts_use_case import ResetPostsUseCase
from entrypoints.api.schemas.create_post import CreatePost, CreatePostResponse
from entrypoints.api.schemas.post_filters import PostFilters
from entrypoints.api.schemas.post_schemas import (
    CountResponse,
    MessageResponse,
    PostResponse,
)

router = APIRouter(prefix="/posts")


@router.post("", response_model=CreatePostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    body: CreatePost, use_case: BaseUseCase = Depends(build_create_post_use_case)
):
    """Create a new post."""
    post = await use_case.execute(body)
    return CreatePostResponse.from_post(post)


@router.get("", response_model=list[PostResponse], status_code=status.HTTP_200_OK)
async def get_all_posts(
    expire: bool | None = Query(
        default=None,
        description="Filtra por publicaciones expiradas o no expiradas",
    ),
    route: str | None = Query(
        default=None,
        min_length=1,
        description="ID del trayecto que se desea usar para el envío",
    ),
    owner: str | None = Query(
        default=None,
        min_length=1,
        description="ID del usuario dueño de la publicación",
    ),
    use_case: GetPostFiltersUseCase = Depends(build_get_post_filter_use_case),
):
    """Retorna el listado de publicaciones que coinciden con los parámetros brindados."""
    filters = PostFilters(expire=expire, route=route, owner=owner)
    posts = await use_case.execute(filters)
    return [PostResponse.from_post(post) for post in posts]


@router.get("/count", response_model=CountResponse)
async def count_posts(
    use_case: CountPostsUseCase = Depends(build_count_posts_use_case),
) -> CountResponse:
    """Return how many users are currently stored."""
    count = await use_case.execute()
    return CountResponse(count=count)


@router.get("/ping", response_class=PlainTextResponse)
def ping():
    """Healthcheck endpoint."""
    return "pong"


@router.post("/reset", response_model=MessageResponse)
async def reset_posts(
    use_case: ResetPostsUseCase = Depends(build_reset_posts_use_case),
) -> MessageResponse:
    """Delete every stored user."""
    await use_case.execute()
    return MessageResponse(msg="Todos los datos fueron eliminados")


@router.get("/{id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def get_post_by_id(
    id: UUID = Path(
        ...,
        description="Identificador de la publicación en formato UUID",
    ),
    use_case: GetPostUseCase = Depends(build_get_post_by_id_use_case),
):
    """Retorna una publicación según el identificador provisto."""
    post = await use_case.execute(str(id))
    return PostResponse.from_post(post)


@router.delete(
    "/{id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_post(
    id: UUID = Path(
        description="Identificador de la publicación en formato UUID",
    ),
    use_case: DeletePostUseCase = Depends(build_delete_post_use_case),
):
    """Elimina una publicación por su ID."""
    await use_case.execute(str(id))
    return MessageResponse(msg="la publicación fue eliminada")
