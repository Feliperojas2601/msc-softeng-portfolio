from fastapi import Depends

from adapters.http.notifications_adapter import HttpNotificationsAdapter
from adapters.http.users_adapter import HttpUsersAdapter
from config import settings
from domain.ports.notifications_port import NotificationsPort
from domain.ports.users_port import UsersPort
from domain.use_cases.process_verification_callback_use_case import (
    ProcessVerificationCallbackUseCase,
)


def build_users_port() -> UsersPort:
    """Build the users_app HTTP adapter."""
    return HttpUsersAdapter(
        settings.users_app_base_url,
        settings.http_timeout_seconds,
        settings.http_max_retries,
    )


def build_notifications_port() -> NotificationsPort:
    """Build the notifications HTTP adapter."""
    return HttpNotificationsAdapter(
        settings.notifications_app_url,
        settings.http_timeout_seconds,
        settings.http_max_retries,
    )


def build_process_verification_callback_use_case(
    users: UsersPort = Depends(build_users_port),
    notifications: NotificationsPort = Depends(build_notifications_port),
) -> ProcessVerificationCallbackUseCase:
    """Build the use case that processes TrueNative's identity verification callback."""
    return ProcessVerificationCallbackUseCase(
        users, notifications, settings.true_native_secret_token
    )
