from adapters.http.client import request
from domain.models.caller import Caller
from domain.ports.users_port import UsersPort
from errors import DownstreamUnavailableError, InvalidTokenError


class HttpUsersAdapter(UsersPort):
    """Servicio de adaptador para la gestión de usuarios a través de la API HTTP."""

    def __init__(self, base_url: str, timeout: float, max_retries: int):
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries

    async def get_me(self, token: str) -> Caller:
        """Obtiene la información del usuario autenticado a partir de un token."""
        response = await request(
            "GET",
            f"{self._base_url}/users/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=self._timeout,
            max_retries=self._max_retries,
        )

        if response.status_code in (401, 403):
            raise InvalidTokenError()
        if response.status_code != 200:
            raise DownstreamUnavailableError()

        body = response.json()
        return Caller(id=body["id"], status=body.get("status"))
