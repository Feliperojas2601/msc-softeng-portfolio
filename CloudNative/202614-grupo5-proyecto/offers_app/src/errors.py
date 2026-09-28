class OfferNotFoundError(Exception):
    """Raised when the offer is not found."""


class InvalidOfferError(Exception):
    """Raised when an offer's values are outside the expected range."""

    def __init__(self, message: str = "Los valores de la oferta no son válidos"):
        self.message = message
        super().__init__(self.message)
