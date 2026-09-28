from adapters.sns.sns_notification_publisher_adapter import (
    SnsNotificationPublisherAdapter,
)
from assembly import build_notification_publisher_port, build_send_notification_use_case
from domain.use_cases.send_notification_use_case import SendNotificationUseCase


def test_build_notification_publisher_port_returns_an_sns_adapter():
    """build_notification_publisher_port wires an SnsNotificationPublisherAdapter."""
    assert isinstance(
        build_notification_publisher_port(), SnsNotificationPublisherAdapter
    )


def test_build_send_notification_use_case_wires_the_use_case():
    """The use case builder returns a use case wired to the publisher port."""
    publisher = build_notification_publisher_port()

    use_case = build_send_notification_use_case(publisher)

    assert isinstance(use_case, SendNotificationUseCase)
    assert use_case.publisher is publisher
