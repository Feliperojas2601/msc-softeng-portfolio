class InvalidSignatureError(Exception):
    """Raised when a callback's verifyToken does not match the expected signature."""


class UserNotFoundError(Exception):
    """Raised when users_app has no user matching the given id."""


class DownstreamUnavailableError(Exception):
    """Raised when a downstream HTTP service cannot be reached or errors out."""
