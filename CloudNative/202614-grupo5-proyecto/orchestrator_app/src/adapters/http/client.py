import logging
from datetime import UTC, datetime

import httpx

from errors import DownstreamUnavailableError

logger = logging.getLogger(__name__)

_RETRYABLE_METHODS = {"GET"}


async def request(
    method: str,
    url: str,
    *,
    timeout: float,
    max_retries: int,
    **kwargs,
) -> httpx.Response:
    """Realiza una llamada HTTP con reintentos para métodos idempotentes (GET).

    Args:
        method: Método HTTP.
        url: URL absoluta a la que se hará la llamada.
        timeout: Tiempo máximo de espera para cada intento.
        max_retries: Número máximo de reintentos para métodos idempotentes.
        **kwargs: Parámetros adicionales para ``httpx.AsyncClient.request``.

    Returns:
        httpx.Response: La respuesta HTTP del servicio downstream.

    Raises:
        DownstreamUnavailableError: El servicio downstream no pudo ser alcanzado después de los reintentos.
    """
    attempts = max_retries + 1 if method.upper() in _RETRYABLE_METHODS else 1
    last_error: Exception | None = None

    for attempt in range(1, attempts + 1):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                return await client.request(method, url, **kwargs)
        except httpx.HTTPError as error:
            last_error = error
            logger.warning(
                "Downstream call %s %s failed (attempt %d/%d): %s",
                method,
                url,
                attempt,
                attempts,
                error,
            )

    raise DownstreamUnavailableError() from last_error


def parse_datetime(value: str) -> datetime:
    """Parsea un string en formato ISO 8601 a un objeto datetime con zona horaria UTC."""
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed
