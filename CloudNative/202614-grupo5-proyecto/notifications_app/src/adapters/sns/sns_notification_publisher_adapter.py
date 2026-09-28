import logging

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from domain.ports.notification_publisher_port import NotificationPublisherPort
from errors import NotificationPublishError

logger = logging.getLogger(__name__)


class SnsNotificationPublisherAdapter(NotificationPublisherPort):
    """Publishes notifications to an AWS SNS Topic.

    The Topic has an email subscription pointing at EMAIL_TO_NOTIFY (created
    by Terraform); SNS delivers the email itself, this adapter only needs
    `sns:Publish`. Credentials are read by boto3 from the environment
    (AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY/AWS_SESSION_TOKEN) — the same
    temporary session credentials the pipeline already uses for Terraform,
    injected as a Kubernetes Secret. No IAM role is created for this.
    """

    def __init__(self, topic_arn: str, region: str):
        self._topic_arn = topic_arn
        self._client = boto3.client("sns", region_name=region)

    async def publish(self, *, subject: str, message: str) -> None:
        """Publish a message to the configured SNS Topic."""
        try:
            self._client.publish(
                TopicArn=self._topic_arn, Subject=subject, Message=message
            )
        except (ClientError, BotoCoreError) as error:
            logger.error("Failed to publish notification to SNS: %s", error)
            raise NotificationPublishError(str(error)) from error
