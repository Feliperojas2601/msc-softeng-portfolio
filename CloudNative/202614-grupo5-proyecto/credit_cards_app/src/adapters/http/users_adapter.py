import httpx

from domain.ports.users_port import UsersPort
from errors import InvalidTokenError, UsersUnavailableError


class HttpUsersAdapter(UsersPort):
    def __init__(self, base_url: str, timeout: float):
        self.url = f"{base_url.rstrip('/')}/users/me"
        self.timeout = timeout

    def get_user_id(self, token: str) -> str:
        try:
            response = httpx.get(
                self.url,
                headers={"Authorization": f"Bearer {token}"},
                timeout=self.timeout,
                follow_redirects=False,
            )
        except httpx.RequestError as exc:
            raise UsersUnavailableError() from exc
        if response.status_code in (401, 403):
            raise InvalidTokenError()
        if response.status_code != 200:
            raise UsersUnavailableError()
        try:
            user = response.json()
        except ValueError as exc:
            raise UsersUnavailableError() from exc
        if not isinstance(user, dict):
            raise UsersUnavailableError()
        user_id = user.get("id")
        if not isinstance(user_id, str) or not user_id.strip():
            raise UsersUnavailableError()
        return user_id
