from adapters.http.client import request
from domain.models.offer import OfferSize
from domain.ports.score_port import ScorePort
from errors import DownstreamUnavailableError


class HttpScoreAdapter(ScorePort):
    """Servicio de adaptador para la gestión de scores a través de la API HTTP."""

    def __init__(self, base_url: str, timeout: float, max_retries: int):
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries

    async def create_score(
        self,
        *,
        offer_id: str,
        size: OfferSize,
        offer: float,
        bag_cost: float,
    ) -> None:
        """Crea el score en el servicio de score."""
        response = await request(
            "POST",
            f"{self._base_url}/scores",
            json={
                "offerId": offer_id,
                "size": size.value,
                "offer": offer,
                "bagCost": bag_cost,
            },
            timeout=self._timeout,
            max_retries=self._max_retries,
        )

        if response.status_code != 201:
            raise DownstreamUnavailableError()

    async def get_score(self, offer_id: str) -> float | None:
        """Obtiene la utilidad de una oferta; nunca lanza, retorna None si falla."""
        try:
            response = await request(
                "GET",
                f"{self._base_url}/scores/{offer_id}",
                timeout=self._timeout,
                max_retries=self._max_retries,
            )
        except DownstreamUnavailableError:
            return None

        if response.status_code != 200:
            return None

        try:
            return float(response.json()["utility"])
        except (KeyError, TypeError, ValueError):
            return None
