from abc import ABC, abstractmethod


class BaseUseCase(ABC):
    """Caso de uso base."""

    @abstractmethod
    def execute(self, *args, **kwargs):
        """Ejecuta el caso de uso."""
