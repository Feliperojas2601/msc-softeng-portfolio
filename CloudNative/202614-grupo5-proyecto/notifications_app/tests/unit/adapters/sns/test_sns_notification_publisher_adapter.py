from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from adapters.sns.sns_notification_publisher_adapter import (
    SnsNotificationPublisherAdapter,
)
from errors import NotificationPublishError

TOPIC_ARN = "arn:aws:sns:us-east-1:000000000000:test-topic"


@pytest.fixture
def boto_client() -> MagicMock:
    """A mocked boto3 SNS client, injected in place of the real one."""
    with patch("adapters.sns.sns_notification_publisher_adapter.boto3") as boto3_mock:
        client = MagicMock()
        boto3_mock.client.return_value = client
        yield client


@pytest.fixture
def adapter(boto_client) -> SnsNotificationPublisherAdapter:
    """An adapter with its boto3 client mocked."""
    return SnsNotificationPublisherAdapter(TOPIC_ARN, "us-east-1")


async def test_publish_calls_sns_with_topic_subject_and_message(adapter, boto_client):
    """publish() calls SNS Publish with the configured Topic ARN and the given content."""
    await adapter.publish(subject="Hello", message="World")

    boto_client.publish.assert_called_once_with(
        TopicArn=TOPIC_ARN, Subject="Hello", Message="World"
    )


async def test_publish_raises_notification_publish_error_on_client_error(
    adapter, boto_client
):
    """A ClientError from SNS is translated into NotificationPublishError."""
    boto_client.publish.side_effect = ClientError(
        {"Error": {"Code": "Throttling", "Message": "slow down"}}, "Publish"
    )

    with pytest.raises(NotificationPublishError):
        await adapter.publish(subject="Hello", message="World")
