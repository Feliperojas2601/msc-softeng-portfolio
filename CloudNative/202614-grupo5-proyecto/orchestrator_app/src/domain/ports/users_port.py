from abc import ABC, abstractmethod

from domain.models.caller import Caller


class UsersPort(ABC):
    """Interfaz para interactuar con el servicio de usuarios."""

    @abstractmethod
    async def get_me(self, token: str) -> Caller:
        """Obtiene la información del usuario autenticado a partir de un token.

        Args:
            token: Token de autenticación del usuario.

        Returns:
            Caller: Información del usuario autenticado.

        Raises:
            InvalidTokenError: El token no es válido o ha expirado.
            DownstreamUnavailableError: El servicio de usuarios no pudo ser alcanzado.
        """
