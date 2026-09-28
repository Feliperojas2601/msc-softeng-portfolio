class NotificationPublishError(Exception):
    """Raised when the notification could not be published (e.g., SNS unreachable)."""
