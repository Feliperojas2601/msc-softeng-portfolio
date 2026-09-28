from adapters.http.client import request
from domain.ports.users_port import UsersPort
from errors import DownstreamUnavailableError, UserNotFoundError


class HttpUsersAdapter(UsersPort):
    """HTTP adapter for users_app: reads contact data, writes final status."""

    def __init__(self, base_url: str, timeout: float, max_retries: int):
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries

    async def get_user(self, user_id: str) -> dict:
        """Fetch a user's public profile (id, email, fullName, dni, phoneNumber)."""
        response = await request(
            "GET",
            f"{self._base_url}/users/{user_id}",
            timeout=self._timeout,
            max_retries=self._max_retries,
        )

        if response.status_code == 404:
            raise UserNotFoundError(user_id)
        if response.status_code != 200:
            raise DownstreamUnavailableError(
                f"users_app returned {response.status_code}"
            )
        return response.json()

    async def update_status(self, user_id: str, status: str) -> None:
        """Set a user's final verification status (VERIFICADO or NO_VERIFICADO)."""
        response = await request(
            "PATCH",
            f"{self._base_url}/users/{user_id}",
            timeout=self._timeout,
            max_retries=self._max_retries,
            json={"status": status},
        )

        if response.status_code == 404:
            raise UserNotFoundError(user_id)
        if response.status_code != 200:
            raise DownstreamUnavailableError(
                f"users_app returned {response.status_code}"
            )
