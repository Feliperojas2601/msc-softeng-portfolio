class RouteAlreadyExistsError(Exception):
    """Raised when a route already exists for a flight id."""


class InvalidRouteDatesError(Exception):
    """Raised when route dates are in the past or out of order."""


class RouteNotFoundError(Exception):
    """Raised when a route cannot be found by id."""
