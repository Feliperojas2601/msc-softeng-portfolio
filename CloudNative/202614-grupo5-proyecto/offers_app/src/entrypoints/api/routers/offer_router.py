from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, status
from fastapi.responses import PlainTextResponse

from assembly import (
    build_count_offers_use_case,
    build_create_offer_use_case,
    build_delete_offer_use_case,
    build_get_offer_by_id_use_case,
    build_get_offer_filter_use_case,
    build_reset_offers_use_case,
)
from domain.use_cases.base_use_case import BaseUseCase
from domain.use_cases.count_offers_use_case import CountOffersUseCase
from domain.use_cases.delete_offer_use_case import DeleteOfferUseCase
from domain.use_cases.get_offer_filter_use_case import GetOfferFiltersUseCase
from domain.use_cases.get_offer_use_case import GetOfferUseCase
from domain.use_cases.reset_offers_use_case import ResetOffersUseCase
from entrypoints.api.schemas.create_offer import CreateOffer, CreateOfferResponse
from entrypoints.api.schemas.offer_filters import OfferFilters
from entrypoints.api.schemas.offer_schemas import (
    CountResponse,
    MessageResponse,
    OfferResponse,
)

router = APIRouter(prefix="/offers")


@router.post(
    "", response_model=CreateOfferResponse, status_code=status.HTTP_201_CREATED
)
async def create_offer(
    body: CreateOffer, use_case: BaseUseCase = Depends(build_create_offer_use_case)
):
    """Create a new offer."""
    offer = await use_case.execute(body)
    return CreateOfferResponse.from_offer(offer)


@router.get("", response_model=list[OfferResponse], status_code=status.HTTP_200_OK)
async def get_all_offers(
    post: str | None = Query(
        default=None,
        min_length=1,
        description="ID de la publicación que se desea usar para el envío",
    ),
    owner: str | None = Query(
        default=None,
        min_length=1,
        description="Identificador del usuario dueño de la oferta",
    ),
    use_case: GetOfferFiltersUseCase = Depends(build_get_offer_filter_use_case),
):
    """Retorna el listado de ofertas que coinciden con los parámetros brindados."""
    filters = OfferFilters(post=post, owner=owner)
    offers = await use_case.execute(filters)
    return [OfferResponse.from_offer(offer) for offer in offers]


@router.get("/count", response_model=CountResponse)
async def count_offers(
    use_case: CountOffersUseCase = Depends(build_count_offers_use_case),
) -> CountResponse:
    """Return how many offers are currently stored."""
    count = await use_case.execute()
    return CountResponse(count=count)


@router.get("/ping", response_class=PlainTextResponse)
def ping():
    """Healthcheck endpoint."""
    return "pong"


@router.post("/reset", response_model=MessageResponse)
async def reset_offers(
    use_case: ResetOffersUseCase = Depends(build_reset_offers_use_case),
) -> MessageResponse:
    """Delete every stored offer."""
    await use_case.execute()
    return MessageResponse(msg="las ofertas fueron eliminadas")


@router.get("/{id}", response_model=OfferResponse, status_code=status.HTTP_200_OK)
async def get_offer_by_id(
    id: UUID = Path(..., description="Identificador de la oferta en formato UUID"),
    use_case: GetOfferUseCase = Depends(build_get_offer_by_id_use_case),
):
    """Retorna una oferta según el identificador provisto."""
    offer = await use_case.execute(str(id))
    return OfferResponse.from_offer(offer)


@router.delete(
    "/{id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_offer(
    id: UUID = Path(description="Identificador de la oferta en formato UUID"),
    use_case: DeleteOfferUseCase = Depends(build_delete_offer_use_case),
):
    """Elimina una oferta por su ID."""
    await use_case.execute(str(id))
    return MessageResponse(msg="la oferta fue eliminada")
