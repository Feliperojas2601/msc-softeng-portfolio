from datetime import datetime
from typing import Any

from adapters.http.client import parse_datetime, request
from domain.models.post import CreatePost, Post
from domain.ports.posts_port import PostsPort
from errors import DownstreamUnavailableError, PostNotFoundError


class HttpPostsAdapter(PostsPort):
    """Servicio de adaptador para la gestión de publicaciones a través de la API HTTP."""

    def __init__(self, base_url: str, timeout: float, max_retries: int):
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries

    async def create_post(
        self,
        user_id: str,
        route_id: str,
        expire_at: datetime,
    ) -> CreatePost:
        """Crea una nueva publicación mediante POST /posts."""
        payload = {
            "routeId": str(route_id),
            "userId": str(user_id),
            "expireAt": expire_at.isoformat(),
        }

        try:
            response = await request(
                "POST",
                f"{self._base_url}/posts",
                json=payload,
                timeout=self._timeout,
                max_retries=self._max_retries,
            )
        except Exception as exc:
            raise DownstreamUnavailableError() from exc

        if response.status_code not in (200, 201):
            raise DownstreamUnavailableError()

        return CreatePost.model_validate(response.json())

    async def get_post(self, post_id: str) -> Post:
        """Busca una publicación por su identificador en el servicio de publicaciones."""
        try:
            response = await request(
                "GET",
                f"{self._base_url}/posts/{post_id}",
                timeout=self._timeout,
                max_retries=self._max_retries,
            )
        except Exception as exc:
            raise DownstreamUnavailableError() from exc

        if response.status_code == 404:
            raise PostNotFoundError()
        if response.status_code != 200:
            raise DownstreamUnavailableError()

        body = response.json()
        return Post(
            id=body["id"],
            route_id=body["routeId"],
            user_id=body["userId"],
            expire_at=parse_datetime(body["expireAt"]),
            created_at=parse_datetime(body["createdAt"]),
        )

    async def get_posts(
        self,
        expire: bool | None = None,
        route: str | None = None,
        owner: str | None = None,
    ) -> list[Post]:
        """Obtiene una lista de publicaciones filtradas desde el servicio downstream."""
        params: dict[str, Any] = {}

        if expire is not None:
            params["expire"] = str(expire).lower()
        if route:
            params["route"] = route
        if owner:
            params["owner"] = owner

        try:
            response = await request(
                "GET",
                f"{self._base_url}/posts",
                params=params,
                timeout=self._timeout,
                max_retries=self._max_retries,
            )
        except Exception as exc:
            raise DownstreamUnavailableError() from exc

        if response.status_code != 200:
            raise DownstreamUnavailableError()

        body = response.json()
        return [
            Post(
                id=item["id"],
                route_id=item["routeId"],
                user_id=item["userId"],
                expire_at=parse_datetime(item["expireAt"]),
                created_at=parse_datetime(item["createdAt"]),
            )
            for item in body
        ]
