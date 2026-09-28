from abc import ABC, abstractmethod


class NotificationPublisherPort(ABC):
    """Port for delivering a notification message to its final destination."""

    @abstractmethod
    async def publish(self, *, subject: str, message: str) -> None:
        """Publish a notification.

        Args:
            subject: Short summary of the notification (e.g., an email subject).
            message: Full body of the notification.

        Raises:
            NotificationPublishError: The message could not be published.
        """
