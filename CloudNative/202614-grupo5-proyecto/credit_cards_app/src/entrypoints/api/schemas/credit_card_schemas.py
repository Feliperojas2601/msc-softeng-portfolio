from datetime import UTC, datetime

from domain.models.credit_card import CreditCard


def format_date(value: datetime) -> str:
    if value.tzinfo is not None:
        value = value.astimezone(UTC).replace(tzinfo=None)
    return value.isoformat(timespec="seconds")


def serialize_credit_card(card: CreditCard) -> dict[str, str]:
    return {
        "id": card.id,
        "token": card.token,
        "userId": card.user_id,
        "lastFourDigits": card.last_four_digits,
        "issuer": card.issuer.value,
        "status": card.status.value,
        "createdAt": format_date(card.created_at),
        "updatedAt": format_date(card.updated_at),
    }
