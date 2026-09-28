from fastapi import APIRouter, Depends, status
from fastapi.responses import PlainTextResponse

from assembly import build_create_score_use_case, build_get_score_use_case
from domain.use_cases.create_score_use_case import CreateScoreUseCase
from domain.use_cases.get_score_use_case import GetScoreUseCase
from entrypoints.api.schemas.create_score import CreateScore, CreateScoreResponse
from entrypoints.api.schemas.score_schemas import ScoreResponse

router = APIRouter(prefix="/scores")


@router.post(
    "", response_model=CreateScoreResponse, status_code=status.HTTP_201_CREATED
)
async def create_score(
    body: CreateScore,
    use_case: CreateScoreUseCase = Depends(build_create_score_use_case),
) -> CreateScoreResponse:
    """Calcula y persiste la utilidad (score) de una oferta."""
    score = await use_case.execute(body)
    return CreateScoreResponse.from_score(score)


@router.get("/ping", response_class=PlainTextResponse)
def ping():
    """Healthcheck endpoint."""
    return "pong"


@router.get(
    "/{offer_id}", response_model=ScoreResponse, status_code=status.HTTP_200_OK
)
async def get_score_by_offer_id(
    offer_id: str, use_case: GetScoreUseCase = Depends(build_get_score_use_case)
) -> ScoreResponse:
    """Retorna el score asociado a una oferta, si ya fue calculado."""
    score = await use_case.execute(offer_id)
    return ScoreResponse.from_score(score)
