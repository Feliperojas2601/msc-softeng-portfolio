from unittest.mock import AsyncMock

import pytest

from domain.use_cases.send_notification_use_case import SendNotificationUseCase


@pytest.fixture
def publisher() -> AsyncMock:
    """A mocked NotificationPublisherPort."""
    return AsyncMock()


@pytest.fixture
def use_case(publisher) -> SendNotificationUseCase:
    """A use case wired to a mocked publisher."""
    return SendNotificationUseCase(publisher)


async def test_identity_verification_publishes_status_and_ruv(use_case, publisher):
    """An identity verification result is published with status, RUV and user data."""
    await use_case.execute(
        type="IDENTITY_VERIFICATION",
        user_id="u1",
        email="john@example.com",
        full_name="John Doe",
        status="VERIFICADO",
        ruv="r1",
    )

    publisher.publish.assert_awaited_once()
    kwargs = publisher.publish.await_args.kwargs
    assert "VERIFICADO" in kwargs["message"]
    assert "r1" in kwargs["message"]
    assert "john@example.com" in kwargs["message"]
    assert "identidad" in kwargs["subject"].lower()


async def test_identity_verification_without_full_name_still_publishes(
    use_case, publisher
):
    """A missing full name does not break the message; it just uses a generic greeting."""
    await use_case.execute(
        type="IDENTITY_VERIFICATION",
        user_id="u1",
        email="john@example.com",
        full_name=None,
        status="NO_VERIFICADO",
        ruv="r1",
    )

    publisher.publish.assert_awaited_once()


async def test_credit_card_verification_publishes_card_details(use_case, publisher):
    """A credit card result is published with status, RUV and the card's basic data."""
    await use_case.execute(
        type="CREDIT_CARD_VERIFICATION",
        user_id="u2",
        email="jane@example.com",
        full_name="Jane Roe",
        status="VERIFICADA",
        ruv="r2",
        last_four_digits="4242",
        franchise="VISA",
    )

    publisher.publish.assert_awaited_once()
    kwargs = publisher.publish.await_args.kwargs
    assert "VERIFICADA" in kwargs["message"]
    assert "r2" in kwargs["message"]
    assert "4242" in kwargs["message"]
    assert "VISA" in kwargs["message"]
    assert "tarjeta" in kwargs["subject"].lower()


async def test_credit_card_rejected_status_is_forwarded_as_is(use_case, publisher):
    """A RECHAZADA result is published the same way as a VERIFICADA one."""
    await use_case.execute(
        type="CREDIT_CARD_VERIFICATION",
        user_id="u2",
        email="jane@example.com",
        full_name=None,
        status="RECHAZADA",
        ruv="r2",
        last_four_digits="4242",
        franchise="VISA",
    )

    kwargs = publisher.publish.await_args.kwargs
    assert "RECHAZADA" in kwargs["message"]
