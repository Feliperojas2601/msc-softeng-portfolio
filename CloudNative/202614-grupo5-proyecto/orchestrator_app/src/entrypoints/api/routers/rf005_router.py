from fastapi import APIRouter, Depends, Path, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from assembly import build_get_post_rf005_use_case
from domain.use_cases.get_post_rf005_use_case import GetPostRf005UseCase
from entrypoints.api.schemas.rf005_schemas import Rf005Response

router = APIRouter(prefix="/rf005")
bearer_scheme = HTTPBearer(auto_error=False)


@router.get(
    "/posts/{post_id}",
    response_model=Rf005Response,
    response_model_by_alias=True,
    status_code=status.HTTP_200_OK,
)
async def get_post_rf005(
    post_id: str = Path(description="Identificador de la publicación"),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    use_case: GetPostRf005UseCase = Depends(build_get_post_rf005_use_case),
) -> Rf005Response:
    """RF-005: consulta una publicación con sus ofertas ordenadas por utilidad."""
    token = credentials.credentials if credentials else None
    detail = await use_case.execute(token=token, post_id=post_id)
    return Rf005Response.from_post_detail(detail)
