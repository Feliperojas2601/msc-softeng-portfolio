from datetime import datetime

from pydantic import BaseModel, ConfigDict

from domain.models.offer import OfferSize
from domain.models.post_detail import PostDetail


class LocationData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    airportCode: str
    country: str


class RouteData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    flightId: str
    origin: LocationData
    destiny: LocationData
    bagCost: float


class OfferData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    userId: str
    description: str
    size: OfferSize
    fragile: bool
    offer: float
    score: float | None
    createdAt: datetime


class PostDetailData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    expireAt: datetime
    route: RouteData
    plannedStartDate: datetime | None
    plannedEndDate: datetime | None
    createdAt: datetime
    offers: list[OfferData]


class Rf005Response(BaseModel):
    """Respuesta de RF-005."""

    model_config = ConfigDict(populate_by_name=True)

    data: PostDetailData

    @classmethod
    def from_post_detail(cls, detail: PostDetail) -> "Rf005Response":
        """Construye la respuesta a partir del agregado devuelto por el caso de uso."""
        return cls(
            data=PostDetailData(
                id=detail.post.id,
                expireAt=detail.post.expire_at,
                route=RouteData(
                    id=detail.route.id,
                    flightId=detail.route.flight_id,
                    origin=LocationData(
                        airportCode=detail.route.source_airport_code,
                        country=detail.route.source_country,
                    ),
                    destiny=LocationData(
                        airportCode=detail.route.destiny_airport_code,
                        country=detail.route.destiny_country,
                    ),
                    bagCost=detail.route.bag_cost,
                ),
                plannedStartDate=detail.route.planned_start_date,
                plannedEndDate=detail.route.planned_end_date,
                createdAt=detail.post.created_at,
                offers=[
                    OfferData(
                        id=item.offer.id,
                        userId=item.offer.user_id,
                        description=item.offer.description,
                        size=item.offer.size,
                        fragile=item.offer.fragile,
                        offer=item.offer.offer,
                        score=item.score,
                        createdAt=item.offer.created_at,
                    )
                    for item in detail.offers
                ],
            )
        )
