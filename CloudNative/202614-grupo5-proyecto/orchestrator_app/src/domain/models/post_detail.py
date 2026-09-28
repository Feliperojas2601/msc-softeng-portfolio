from pydantic import BaseModel, ConfigDict

from domain.models.offer import Offer
from domain.models.post import Post
from domain.models.route import RouteDetail


class OfferWithScore(BaseModel):
    """Una oferta con su utilidad (score), o None si no se pudo obtener (RF-005)."""

    model_config = ConfigDict(populate_by_name=True)

    offer: Offer
    score: float | None = None


class PostDetail(BaseModel):
    """Resultado agregado de RF-005: publicación, trayecto y ofertas con utilidad."""

    model_config = ConfigDict(populate_by_name=True)

    post: Post
    route: RouteDetail
    offers: list[OfferWithScore]
