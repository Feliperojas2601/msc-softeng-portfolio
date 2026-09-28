from abc import ABC, abstractmethod

from domain.models.offer import OfferSize


class ScorePort(ABC):
    """Interfaz para interactuar con el servicio de puntuación/score."""

    @abstractmethod
    async def create_score(
        self,
        *,
        offer_id: str,
        size: OfferSize,
        offer: float,
        bag_cost: float,
    ) -> None:
        """Crea la puntuación/score de una oferta en el servicio de puntuación/score.

        El orquestador entrega todas las entradas de la fórmula. El servicio de
        score aplica la fórmula y persiste el resultado; no consulta a ningún
        otro servicio de dominio.

        Args:
            offer_id: Identificador de la oferta para la cual se crea la puntuación/score.
            size: Tamaño del paquete, una entrada del porcentaje de ocupación.
            offer: Cantidad propuesta para el envío, una entrada de la fórmula.
            bag_cost: Costo de la maleta en el trayecto, obtenido por el orquestador.

        Raises:
            DownstreamUnavailableError: El servicio de puntuación/score no pudo ser alcanzado.
        """

    @abstractmethod
    async def get_score(self, offer_id: str) -> float | None:
        """Obtiene la utilidad (score) ya calculada de una oferta.

        Args:
            offer_id: Identificador de la oferta.

        Returns:
            float | None: La utilidad de la oferta, o None si no está disponible.
        """
