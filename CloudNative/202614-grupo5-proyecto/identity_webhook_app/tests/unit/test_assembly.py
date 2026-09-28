from adapters.http.notifications_adapter import HttpNotificationsAdapter
from adapters.http.users_adapter import HttpUsersAdapter
from assembly import (
    build_notifications_port,
    build_process_verification_callback_use_case,
    build_users_port,
)
from domain.use_cases.process_verification_callback_use_case import (
    ProcessVerificationCallbackUseCase,
)


def test_build_users_port_returns_an_http_users_adapter():
    """build_users_port wires an HttpUsersAdapter from settings."""
    assert isinstance(build_users_port(), HttpUsersAdapter)


def test_build_notifications_port_returns_an_http_notifications_adapter():
    """build_notifications_port wires an HttpNotificationsAdapter from settings."""
    assert isinstance(build_notifications_port(), HttpNotificationsAdapter)


def test_build_process_verification_callback_use_case_wires_the_use_case():
    """The use case builder returns a use case wired to both ports."""
    users = build_users_port()
    notifications = build_notifications_port()

    use_case = build_process_verification_callback_use_case(users, notifications)

    assert isinstance(use_case, ProcessVerificationCallbackUseCase)
    assert use_case.users is users
    assert use_case.notifications is notifications
