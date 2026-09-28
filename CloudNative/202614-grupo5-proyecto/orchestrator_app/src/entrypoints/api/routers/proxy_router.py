import httpx
from fastapi import APIRouter, Request
from fastapi.responses import Response

from config import settings

"""" Este router sirve para que el orquestador actue como proxy en los despliegues locales """

router = APIRouter()


async def _proxy(method: str, url: str, request: Request) -> Response:
    body = await request.body()
    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            url,
            content=body,
            headers=headers,
            params=dict(request.query_params),
        )
    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type=response.headers.get("content-type"),
    )


# Users
@router.api_route("/users", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_users_root(request: Request):
    return await _proxy(request.method, f"{settings.users_app_url}/users", request)


@router.api_route(
    "/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def proxy_users(path: str, request: Request):
    return await _proxy(
        request.method, f"{settings.users_app_url}/users/{path}", request
    )


# Posts
@router.api_route("/posts", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_posts_root(request: Request):
    return await _proxy(request.method, f"{settings.posts_app_url}/posts", request)


@router.api_route(
    "/posts/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def proxy_posts(path: str, request: Request):
    return await _proxy(
        request.method, f"{settings.posts_app_url}/posts/{path}", request
    )


# Routes
@router.api_route("/routes", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_routes_root(request: Request):
    return await _proxy(request.method, f"{settings.routes_app_url}/routes", request)


@router.api_route(
    "/routes/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def proxy_routes(path: str, request: Request):
    return await _proxy(
        request.method, f"{settings.routes_app_url}/routes/{path}", request
    )


# Offers
@router.api_route("/offers", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_offers_root(request: Request):
    return await _proxy(request.method, f"{settings.offers_app_url}/offers", request)


@router.api_route(
    "/offers/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def proxy_offers(path: str, request: Request):
    return await _proxy(
        request.method, f"{settings.offers_app_url}/offers/{path}", request
    )


# Scores
@router.api_route("/scores", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_scores_root(request: Request):
    return await _proxy(request.method, f"{settings.scores_app_url}/scores", request)


@router.api_route(
    "/scores/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
)
async def proxy_scores(path: str, request: Request):
    return await _proxy(
        request.method, f"{settings.scores_app_url}/scores/{path}", request
    )
