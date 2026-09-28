from fastapi import APIRouter, Depends, Path, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from assembly import build_create_offer_rf004_use_case
from domain.use_cases.create_offer_rf004_use_case import CreateOfferRf004UseCase
from entrypoints.api.schemas.rf004_schemas import CreateOfferRequest, Rf004Response

router = APIRouter(prefix="/rf004")
bearer_scheme = HTTPBearer(auto_error=False)


@router.post(
    "/posts/{post_id}/offers",
    response_model=Rf004Response,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
)
async def create_offer_rf004(
    body: CreateOfferRequest,
    post_id: str = Path(description="Identificador de la publicación"),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    use_case: CreateOfferRf004UseCase = Depends(build_create_offer_rf004_use_case),
) -> Rf004Response:
    """RF-004: crea una oferta para una publicación a través del flujo orquestado."""
    token = credentials.credentials if credentials else None
    offer = await use_case.execute(token=token, post_id=post_id, data=body.to_command())
    return Rf004Response.from_offer(offer, post_id)
