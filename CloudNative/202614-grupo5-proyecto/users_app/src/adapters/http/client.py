import logging

import httpx

from errors import IdentityVerificationRequestError

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
    """Perform an HTTP call, retrying idempotent methods (GET) on transport errors.

    Args:
        method: HTTP method.
        url: Absolute URL to call.
        timeout: Per-attempt timeout, in seconds.
        max_retries: Maximum number of retries for idempotent methods.
        **kwargs: Extra parameters forwarded to httpx.AsyncClient.request.

    Returns:
        The HTTP response from the downstream service.

    Raises:
        IdentityVerificationRequestError: The downstream service could not be
            reached after every attempt.
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

    raise IdentityVerificationRequestError() from last_error
