class OrchestratorError(Exception):
    """Error base para el dominio del orquestador."""

    status_code: int = 500
    default_message: str = "Error interno del orquestador."

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


class MissingTokenError(OrchestratorError):
    """Lanzado cuando la solicitud no contiene un token de autenticación."""

    status_code = 403
    default_message = "No se proporcionó un token de autenticación."


class InvalidTokenError(OrchestratorError):
    """Lanzado cuando el token de autenticación no es válido o ha expirado."""

    status_code = 401
    default_message = "El token no es válido o está vencido."


class InvalidDatesError(OrchestratorError):
    """412: Las fechas del trayecto no son válidas."""

    status_code = 412
    default_message = "Las fechas del trayecto no son válidas"


class InvalidExpirationDateError(OrchestratorError):
    """412: La fecha expiración no es válida."""

    status_code = 412
    default_message = "La fecha expiración no es válida"


class PostNotFoundError(OrchestratorError):
    """Lanzado cuando la publicación solicitada no existe en el servicio de publicaciones."""

    status_code = 404
    default_message = "La publicación no existe."


class DuplicatePostError(OrchestratorError):
    """412: El usuario ya tiene una publicación para la misma fecha/trayecto."""

    status_code = 412
    default_message = "El usuario ya tiene una publicación para la misma fecha"


class PostAccessDeniedError(OrchestratorError):
    """403: el usuario no es el propietario de la publicación consultada."""

    status_code = 403
    default_message = (
        "El usuario no tiene permiso para ver el contenido de esta publicación."
    )


class OfferNotAllowedError(OrchestratorError):
    """Lanzado cuando la oferta no está permitida, por ejemplo, si la publicación ya expiró o el usuario intenta ofertar en su propia publicación."""

    status_code = 412
    default_message = "La oferta no cumple las reglas de negocio."


class DownstreamUnavailableError(OrchestratorError):
    """Lanzado cuando un servicio descendente falla, se agota el tiempo de espera o no es alcanzable."""

    status_code = 503
    default_message = "El servicio está temporalmente fuera de servicio."
