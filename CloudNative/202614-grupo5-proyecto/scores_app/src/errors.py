class ScoreNotFoundError(Exception):
    """Raised when no score is found for the requested offer."""


class InvalidScoreError(Exception):
    """Raised when a score's input values are outside the expected range."""

    def __init__(self, message: str = "Los valores del score no son válidos"):
        self.message = message
        super().__init__(self.message)
