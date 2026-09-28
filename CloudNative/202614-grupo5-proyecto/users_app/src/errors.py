class UserAlreadyExistsError(Exception):
    """Raised when a user with the same username or email already exists."""


class UserNotFoundError(Exception):
    """Raised when a user cannot be found by its identifier."""


class InvalidCredentialsError(Exception):
    """Raised when the provided username/password do not match any user."""


class InvalidTokenError(Exception):
    """Raised when a token is missing from storage or has expired."""


class UserNotVerifiedError(Exception):
    """Raised when a user has not completed identity verification (RF-007)."""


class IdentityVerificationRequestError(Exception):
    """Raised when the call to the external identity verification provider fails."""
