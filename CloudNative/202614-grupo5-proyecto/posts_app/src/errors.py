class ExpirationDateNoValid(Exception):
    """Raised when the expiration date is not in the future or is not valid."""

    def __init__(self, message: str = "La fecha expiración no es válida"):
        self.message = message
        super().__init__(self.message)


class PostNotFoundError(Exception):
    """Raised when the post is not found."""
