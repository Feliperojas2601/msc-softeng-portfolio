from domain.ports.notification_publisher_port import NotificationPublisherPort

IDENTITY_VERIFICATION = "IDENTITY_VERIFICATION"
CREDIT_CARD_VERIFICATION = "CREDIT_CARD_VERIFICATION"


def _build_identity_email(
    user_id: str, email: str, full_name: str | None, status: str, ruv: str
) -> tuple[str, str]:
    """Build the subject and body for an identity verification result (RF-007).

    The Topic's subscriber is a single fixed address (EMAIL_TO_NOTIFY), not
    the user's own inbox, so the body must identify whose result this is.
    """
    greeting = f"Hola {full_name}," if full_name else "Hola,"
    subject = "Resultado de tu verificacion de identidad"
    message = (
        f"{greeting}\n\n"
        f"El resultado de tu verificacion de identidad es: {status}.\n\n"
        f"Codigo de verificacion (RUV): {ruv}\n"
        f"Usuario: {user_id} ({email})"
    )
    return subject, message


def _build_credit_card_email(
    user_id: str,
    email: str,
    full_name: str | None,
    status: str,
    ruv: str,
    last_four_digits: str | None,
    franchise: str | None,
) -> tuple[str, str]:
    """Build the subject and body for a credit card verification result (RF-006).

    The Topic's subscriber is a single fixed address (EMAIL_TO_NOTIFY), not
    the user's own inbox, so the body must identify whose result this is.
    """
    greeting = f"Hola {full_name}," if full_name else "Hola,"
    card = f"{franchise or 'tarjeta'} terminada en {last_four_digits or '????'}"
    subject = "Resultado de la verificacion de tu tarjeta"
    message = (
        f"{greeting}\n\n"
        f"El resultado de la verificacion de tu {card} es: {status}.\n\n"
        f"Codigo de verificacion (RUV): {ruv}\n"
        f"Usuario: {user_id} ({email})"
    )
    return subject, message


class SendNotificationUseCase:
    """Use case for formatting and publishing a result notification.

    Handles both notification types the system produces: identity
    verification (RF-007) and credit card verification (RF-006). Neither
    producer's data is read directly; every field needed to build the
    notification arrives in the request itself.
    """

    def __init__(self, publisher: NotificationPublisherPort):
        self.publisher = publisher

    async def execute(
        self,
        *,
        type: str,
        user_id: str,
        email: str,
        full_name: str | None,
        status: str,
        ruv: str,
        last_four_digits: str | None = None,
        franchise: str | None = None,
    ) -> None:
        """Build and publish the notification for the given event type.

        Args:
            type: IDENTITY_VERIFICATION or CREDIT_CARD_VERIFICATION.
            user_id: Id of the user this notification is about.
            email: The user's own email, included in the body for traceability
                (the Topic's subscriber is a single fixed address, not the
                user's inbox).
            full_name: Recipient's full name, if known.
            status: Final status reported by the producer.
            ruv: TrueNative's verification record identifier.
            last_four_digits: Last 4 digits of the card (CREDIT_CARD_VERIFICATION only).
            franchise: Card franchise/brand (CREDIT_CARD_VERIFICATION only).

        Raises:
            NotificationPublishError: The notification could not be published.
        """
        if type == IDENTITY_VERIFICATION:
            subject, message = _build_identity_email(
                user_id, email, full_name, status, ruv
            )
        else:
            subject, message = _build_credit_card_email(
                user_id, email, full_name, status, ruv, last_four_digits, franchise
            )

        await self.publisher.publish(subject=subject, message=message)
