from abc import ABC, abstractmethod

from domain.models.offer import CreatedOffer, Offer, OfferSize


class OffersPort(ABC):
    """Interfaz para interactuar con el servicio de ofertas."""

    @abstractmethod
    async def get_offers_by_post(self, post_id: str) -> list[Offer]:
        """Obtiene las ofertas hechas sobre una publicación.

        Args:
            post_id: Identificador de la publicación.

        Returns:
            list[Offer]: Las ofertas hechas sobre la publicación.

        Raises:
            DownstreamUnavailableError: El servicio de ofertas no pudo ser alcanzado.
        """

    @abstractmethod
    async def create_offer(
        self,
        *,
        post_id: str,
        user_id: str,
        description: str,
        size: OfferSize,
        fragile: bool,
        offer: float,
    ) -> CreatedOffer:
        """Crea una oferta para una publicación.

        Args:
            post_id: Identificador de la publicación a la que se dirige la oferta.
            user_id: Identificador del usuario que realiza la oferta.
            description: Descripción del paquete a llevar.
            size: Tamaño del paquete.
            fragile: Indica si el paquete es delicado.
            offer: Valor en dólares que se propone por el envío.

        Returns:
            CreatedOffer: La oferta creada, con su identificador y fecha de creación.

        Raises:
            DownstreamUnavailableError: El servicio de ofertas no pudo ser alcanzado.
        """

    @abstractmethod
    async def delete_offer(self, offer_id: str) -> None:
        """Elimina una oferta existente.
           Se utiliza como acción compensatoria en rf004_use_case cuando la creación de la puntuación/score falla.

        Args:
            offer_id: Identificador de la oferta a eliminar.

        Raises:
            DownstreamUnavailableError: El servicio de ofertas no pudo ser alcanzado.
        """
