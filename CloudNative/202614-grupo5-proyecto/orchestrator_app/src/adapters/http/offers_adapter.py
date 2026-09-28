from adapters.http.client import parse_datetime, request
from domain.models.offer import CreatedOffer, Offer, OfferSize
from domain.ports.offers_port import OffersPort
from errors import DownstreamUnavailableError


class HttpOffersAdapter(OffersPort):
    """Servicio de adaptador para la gestión de ofertas a través de la API HTTP."""

    def __init__(self, base_url: str, timeout: float, max_retries: int):
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries

    async def get_offers_by_post(self, post_id: str) -> list[Offer]:
        """Obtiene las ofertas hechas sobre una publicación."""
        try:
            response = await request(
                "GET",
                f"{self._base_url}/offers",
                params={"post": post_id},
                timeout=self._timeout,
                max_retries=self._max_retries,
            )
        except Exception as exc:
            raise DownstreamUnavailableError() from exc

        if response.status_code != 200:
            raise DownstreamUnavailableError()

        return [
            Offer(
                id=item["id"],
                user_id=item["userId"],
                description=item["description"],
                size=item["size"],
                fragile=item["fragile"],
                offer=item["offer"],
                created_at=parse_datetime(item["createdAt"]),
            )
            for item in response.json()
        ]

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
        """Crea la oferta en el servicio de ofertas."""
        response = await request(
            "POST",
            f"{self._base_url}/offers",
            json={
                "postId": post_id,
                "userId": user_id,
                "description": description,
                "size": size.value,
                "fragile": fragile,
                "offer": offer,
            },
            timeout=self._timeout,
            max_retries=self._max_retries,
        )

        if response.status_code != 201:
            raise DownstreamUnavailableError()

        body = response.json()
        return CreatedOffer(
            id=body["id"],
            user_id=body["userId"],
            created_at=parse_datetime(body["createdAt"]),
        )

    async def delete_offer(self, offer_id: str) -> None:
        """Elimina la oferta."""
        response = await request(
            "DELETE",
            f"{self._base_url}/offers/{offer_id}",
            timeout=self._timeout,
            max_retries=self._max_retries,
        )

        if response.status_code not in (200, 404):
            raise DownstreamUnavailableError()
