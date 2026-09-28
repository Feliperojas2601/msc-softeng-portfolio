from fastapi import Depends

from adapters.sns.sns_notification_publisher_adapter import (
    SnsNotificationPublisherAdapter,
)
from config import settings
from domain.ports.notification_publisher_port import NotificationPublisherPort
from domain.use_cases.send_notification_use_case import SendNotificationUseCase


def build_notification_publisher_port() -> NotificationPublisherPort:
    """Build the SNS notification publisher adapter."""
    return SnsNotificationPublisherAdapter(settings.sns_topic_arn, settings.aws_region)


def build_send_notification_use_case(
    publisher: NotificationPublisherPort = Depends(build_notification_publisher_port),
) -> SendNotificationUseCase:
    """Build the use case that formats and publishes result notifications."""
    return SendNotificationUseCase(publisher)
