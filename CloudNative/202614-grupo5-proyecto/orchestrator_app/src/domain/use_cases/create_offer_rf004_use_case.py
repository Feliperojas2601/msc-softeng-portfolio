import logging
from collections.abc import Callable
from datetime import UTC, datetime

from domain.models.offer import CreatedOffer, CreateOfferCommand
from domain.ports.offers_port import OffersPort
from domain.ports.posts_port import PostsPort
from domain.ports.routes_port import RoutesPort
from domain.ports.score_port import ScorePort
from domain.ports.users_port import UsersPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import (
    DownstreamUnavailableError,
    MissingTokenError,
    OfferNotAllowedError,
)

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    """Retorna la fecha y hora actual en UTC."""
    return datetime.now(UTC)


class CreateOfferRf004UseCase(BaseUseCase):
    """RF-004: crea una oferta para una publicación de envío
    orquestando la interacción con los servicios de usuarios, publicaciones, ofertas y puntuación/score.
    """

    def __init__(
        self,
        users: UsersPort,
        posts: PostsPort,
        routes: RoutesPort,
        offers: OffersPort,
        score: ScorePort,
        now_provider: Callable[[], datetime] = _utc_now,
    ):
        self.users = users
        self.posts = posts
        self.routes = routes
        self.offers = offers
        self.score = score
        self.now_provider = now_provider

    async def execute(
        self, token: str | None, post_id: str, data: CreateOfferCommand
    ) -> CreatedOffer:
        """Ejecuta el caso de uso RF-004.

        Args:
            token: El token de autenticación del usuario que realiza la oferta.
            post_id: El identificador de la publicación a la que se dirige la oferta.
            data: Los datos de la oferta a crear, encapsulados en un objeto CreateOfferCommand.

        Returns:
            CreatedOffer: La oferta creada, con su identificador y fecha de creación.

        Raises:
            MissingTokenError: No se proporcionó un token de autenticación.
            InvalidTokenError: El token no es válido o ha expirado.
            PostNotFoundError: La publicación no existe.
            OfferNotAllowedError: La oferta no está permitida (por ejemplo, la publicación ya expiró o el usuario intenta ofertar en su propia publicación).
            DownstreamUnavailableError: El servicio de usuarios, publicaciones, ofertas o puntuación/score no pudo ser alcanzado.
        """
        if not token:
            raise MissingTokenError()

        caller = await self.users.get_me(token)
        post = await self.posts.get_post(post_id)

        if post.expire_at <= self.now_provider():
            raise OfferNotAllowedError("La publicación ya expiró.")
        if post.user_id == caller.id:
            raise OfferNotAllowedError(
                "El usuario no puede ofertar en su propia publicación."
            )

        route = await self.routes.get_route(post.route_id)

        offer = await self.offers.create_offer(
            post_id=post_id,
            user_id=caller.id,
            description=data.description,
            size=data.size,
            fragile=data.fragile,
            offer=data.offer,
        )

        try:
            await self.score.create_score(
                offer_id=offer.id,
                size=data.size,
                offer=data.offer,
                bag_cost=route.bag_cost,
            )
        except DownstreamUnavailableError:
            await self._compensate(offer.id)
            raise

        return offer

    async def _compensate(self, offer_id: str) -> None:
        """Compensación de rf004_use_case: elimina la oferta creada si la creación de la puntuación/score falla."""
        try:
            await self.offers.delete_offer(offer_id)
        except DownstreamUnavailableError:
            logger.warning(
                "La compensación de rf004_use_case falló: la oferta %s no pudo ser "
                "eliminada y quedó sin puntuación/score.",
                offer_id,
            )
