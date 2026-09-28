from fastapi import Depends

from adapters.http.offers_adapter import HttpOffersAdapter
from adapters.http.posts_adapter import HttpPostsAdapter
from adapters.http.routes_adapter import HttpRoutesAdapter
from adapters.http.score_adapter import HttpScoreAdapter
from adapters.http.users_adapter import HttpUsersAdapter
from config import settings
from domain.ports.offers_port import OffersPort
from domain.ports.posts_port import PostsPort
from domain.ports.routes_port import RoutesPort
from domain.ports.score_port import ScorePort
from domain.ports.users_port import UsersPort
from domain.use_cases.create_offer_rf004_use_case import CreateOfferRf004UseCase
from domain.use_cases.create_post_rf003_use_case import CreatePostRf003UseCase
from domain.use_cases.get_post_rf005_use_case import GetPostRf005UseCase


def build_users_port() -> UsersPort:
    """Construye el adaptador del servicio de usuarios."""
    return HttpUsersAdapter(
        settings.users_app_url,
        settings.http_timeout_seconds,
        settings.http_max_retries,
    )


def build_posts_port() -> PostsPort:
    """Construye el adaptador del servicio de publicaciones."""
    return HttpPostsAdapter(
        settings.posts_app_url,
        settings.http_timeout_seconds,
        settings.http_max_retries,
    )


def build_routes_port() -> RoutesPort:
    """Construye el adaptador del servicio de trayectos."""
    return HttpRoutesAdapter(
        settings.routes_app_url,
        settings.http_timeout_seconds,
        settings.http_max_retries,
    )


def build_offers_port() -> OffersPort:
    """Construye el adaptador del servicio de ofertas."""
    return HttpOffersAdapter(
        settings.offers_app_url,
        settings.http_timeout_seconds,
        settings.http_max_retries,
    )


def build_score_port() -> ScorePort:
    """Construye el adaptador del servicio de puntuación."""
    return HttpScoreAdapter(
        settings.scores_app_url,
        settings.http_timeout_seconds,
        settings.http_max_retries,
    )


def build_create_post_rf003_use_case(
    users: UsersPort = Depends(build_users_port),
    posts: PostsPort = Depends(build_posts_port),
    routes: RoutesPort = Depends(build_routes_port),
) -> CreatePostRf003UseCase:
    """Construye el caso de uso para crear un post en RF-003."""
    return CreatePostRf003UseCase(users, posts, routes)


def build_create_offer_rf004_use_case(
    users: UsersPort = Depends(build_users_port),
    posts: PostsPort = Depends(build_posts_port),
    routes: RoutesPort = Depends(build_routes_port),
    offers: OffersPort = Depends(build_offers_port),
    score: ScorePort = Depends(build_score_port),
) -> CreateOfferRf004UseCase:
    """Construye el caso de uso para crear una oferta en RF-004."""
    return CreateOfferRf004UseCase(users, posts, routes, offers, score)


def build_get_post_rf005_use_case(
    users: UsersPort = Depends(build_users_port),
    posts: PostsPort = Depends(build_posts_port),
    routes: RoutesPort = Depends(build_routes_port),
    offers: OffersPort = Depends(build_offers_port),
    score: ScorePort = Depends(build_score_port),
) -> GetPostRf005UseCase:
    """Construye el caso de uso para consultar una publicación en RF-005."""
    return GetPostRf005UseCase(users, posts, routes, offers, score)
