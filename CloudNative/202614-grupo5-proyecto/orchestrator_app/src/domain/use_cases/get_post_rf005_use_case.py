import asyncio

from domain.models.post_detail import OfferWithScore, PostDetail
from domain.ports.offers_port import OffersPort
from domain.ports.posts_port import PostsPort
from domain.ports.routes_port import RoutesPort
from domain.ports.score_port import ScorePort
from domain.ports.users_port import UsersPort
from domain.use_cases.base_use_case import BaseUseCase
from errors import MissingTokenError, PostAccessDeniedError


def _sort_key(item: OfferWithScore) -> tuple[bool, float]:
    """Ordena las ofertas descendente por score; las que no tienen score quedan al final."""
    return (item.score is None, -(item.score or 0.0))


class GetPostRf005UseCase(BaseUseCase):
    """RF-005: consulta una publicación con sus ofertas ordenadas por utilidad,
    orquestando la interacción con los servicios de usuarios, publicaciones,
    rutas, ofertas y puntuación/score.
    """

    def __init__(
        self,
        users: UsersPort,
        posts: PostsPort,
        routes: RoutesPort,
        offers: OffersPort,
        score: ScorePort,
    ):
        self.users = users
        self.posts = posts
        self.routes = routes
        self.offers = offers
        self.score = score

    async def execute(self, token: str | None, post_id: str) -> PostDetail:
        """Ejecuta el caso de uso RF-005.

        Args:
            token: El token de autenticación del usuario que consulta.
            post_id: El identificador de la publicación a consultar.

        Returns:
            PostDetail: La publicación, su trayecto y sus ofertas con utilidad.

        Raises:
            MissingTokenError: No se proporcionó un token de autenticación.
            InvalidTokenError: El token no es válido o ha expirado.
            PostNotFoundError: La publicación no existe.
            PostAccessDeniedError: El usuario no es el propietario de la publicación.
            DownstreamUnavailableError: Un servicio indispensable no pudo ser alcanzado.
        """
        if not token:
            raise MissingTokenError()

        caller = await self.users.get_me(token)
        post = await self.posts.get_post(post_id)

        if post.user_id != caller.id:
            raise PostAccessDeniedError()

        route = await self.routes.get_route_detail(post.route_id)
        offers = await self.offers.get_offers_by_post(post_id)

        scores = await asyncio.gather(
            *(self.score.get_score(offer.id) for offer in offers)
        )
        offers_with_score = [
            OfferWithScore(offer=offer, score=score)
            for offer, score in zip(offers, scores, strict=True)
        ]
        offers_with_score.sort(key=_sort_key)

        return PostDetail(post=post, route=route, offers=offers_with_score)
