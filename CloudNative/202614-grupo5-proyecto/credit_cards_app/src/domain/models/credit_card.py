from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class CreditCardIssuer(StrEnum):
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"
    AMERICAN_EXPRESS = "AMERICAN EXPRESS"
    DISCOVER = "DISCOVER"
    DINERS_CLUB = "DINERS CLUB"
    UNKNOWN = "UNKNOWN"


class CreditCardStatus(StrEnum):
    POR_VERIFICAR = "POR_VERIFICAR"
    RECHAZADA = "RECHAZADA"
    APROBADA = "APROBADA"


@dataclass(slots=True)
class CreditCard:
    id: str
    token: str
    user_id: str
    last_four_digits: str
    ruv: str | None
    issuer: CreditCardIssuer
    status: CreditCardStatus
    created_at: datetime
    updated_at: datetime
