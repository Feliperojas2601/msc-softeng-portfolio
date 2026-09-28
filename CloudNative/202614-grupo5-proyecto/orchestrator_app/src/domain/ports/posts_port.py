from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from domain.models.post import CreatePost, Post


class PostsPort(ABC):
    """Interfaz para interactuar con el servicio de publicaciones."""

    @abstractmethod
    async def create_post(
        self,
        user_id: str | UUID,
        route_id: str | UUID,
        expire_at: datetime,
    ) -> CreatePost:
        """Crea una publicación en el servicio downstream de posts.

        Args:
            user_id: Identificador del usuario creador.
            route_id: Identificador del trayecto (ruta).
            expire_at: Fecha máxima de ofertas en formato datetime.

        Returns:
            CreatedPost: Datos de la publicación creada (id, userId, createdAt).

        Raises:
            DownstreamUnavailableError: El servicio de publicaciones no pudo ser alcanzado.
        """

    @abstractmethod
    async def get_post(self, post_id: str) -> Post:
        """Obtiene una publicación por identificador.

        Args:
            post_id: Identificador de la publicación a obtener.

        Returns:
            Post: La publicación obtenida.

        Raises:
            PostNotFoundError: La publicación no existe.
            DownstreamUnavailableError: El servicio de publicaciones no pudo ser alcanzado.
        """

    @abstractmethod
    async def get_posts(
        self,
        expire: bool | None = None,
        route: str | None = None,
        owner: str | None = None,
    ) -> list[Post]:
        """Obtiene una lista de publicaciones filtradas por expiración, trayecto o dueño.

        Args:
            expire: Filtra si la publicación está expirada o no.
            route: ID del trayecto.
            owner: ID del usuario creador.

        Returns:
            list[PostDetail]: Lista de publicaciones que cumplen los filtros.

        Raises:
            DownstreamUnavailableError: El servicio de publicaciones no pudo ser alcanzado.
        """
