from abc import ABC, abstractmethod


class BaseUseCase(ABC):
    """Base use case class."""

    @abstractmethod
    async def execute(self, *args, **kwargs):
        """Execute the use case."""
        pass
