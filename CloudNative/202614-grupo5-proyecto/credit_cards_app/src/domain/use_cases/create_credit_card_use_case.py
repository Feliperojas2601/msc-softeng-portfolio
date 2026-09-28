import calendar
import re
from datetime import UTC, datetime
from uuid import uuid4

from domain.models.credit_card import CreditCard, CreditCardIssuer, CreditCardStatus
from domain.ports.credit_card_repository_port import CreditCardRepositoryPort
from domain.ports.payment_provider_port import PaymentProviderPort
from errors import (
    DuplicateCardError,
    ExpiredCardError,
    InvalidCardDataError,
    PaymentProviderUnavailableError,
)


class CreateCreditCardUseCase:
    def __init__(
        self,
        repository: CreditCardRepositoryPort,
        payment_provider: PaymentProviderPort,
    ):
        self.repository = repository
        self.payment_provider = payment_provider

    def execute(
        self,
        *,
        user_id: str,
        card_number: str,
        cvv: str,
        expiration_date: str,
        card_holder_name: str,
    ) -> CreditCard:
        self._validate(card_number, cvv, expiration_date, card_holder_name)
        if self._is_expired(expiration_date):
            raise ExpiredCardError()
        result = self.payment_provider.tokenize(
            card_number=card_number,
            cvv=cvv,
            expiration_date=expiration_date,
            card_holder_name=card_holder_name,
        )
        if result.ruv is not None and (
            not isinstance(result.ruv, str)
            or not result.ruv.strip()
            or len(result.ruv) > 256
        ):
            raise PaymentProviderUnavailableError()
        if self.repository.exists_for_user(user_id, result.token):
            raise DuplicateCardError()
        now = datetime.now(UTC)
        card = CreditCard(
            id=str(uuid4()),
            token=result.token,
            user_id=user_id,
            last_four_digits=card_number[-4:],
            ruv=result.ruv,
            issuer=self._issuer(result.issuer, card_number),
            status=CreditCardStatus.POR_VERIFICAR,
            created_at=now,
            updated_at=now,
        )
        return self.repository.create(card)

    @staticmethod
    def _validate(
        card_number: str,
        cvv: str,
        expiration_date: str,
        card_holder_name: str,
    ) -> None:
        if (
            not isinstance(card_number, str)
            or not re.fullmatch(r"[0-9]+", card_number)
            or len(card_number) < 4
        ):
            raise InvalidCardDataError()
        if not isinstance(cvv, str) or not re.fullmatch(r"[0-9]{3,4}", cvv):
            raise InvalidCardDataError()
        if not isinstance(expiration_date, str) or not re.fullmatch(
            r"[0-9]{2}/[0-9]{2}", expiration_date
        ):
            raise InvalidCardDataError()
        month = int(expiration_date[3:])
        if not 1 <= month <= 12:
            raise InvalidCardDataError()
        if not isinstance(card_holder_name, str) or not card_holder_name.strip():
            raise InvalidCardDataError()

    @staticmethod
    def _is_expired(expiration_date: str) -> bool:
        year, month = (int(part) for part in expiration_date.split("/"))
        full_year = 2000 + year
        last_day = calendar.monthrange(full_year, month)[1]
        expiration = datetime(full_year, month, last_day, 23, 59, 59, tzinfo=UTC)
        return datetime.now(UTC) > expiration

    @staticmethod
    def _issuer(value: str, card_number: str) -> CreditCardIssuer:
        normalized = value.strip().upper()
        aliases = {
            "AMERICAN_EXPRESS": "AMERICAN EXPRESS",
            "AMEX": "AMERICAN EXPRESS",
            "DINERS_CLUB": "DINERS CLUB",
        }
        normalized = aliases.get(normalized, normalized)
        try:
            return CreditCardIssuer(normalized)
        except ValueError:
            if card_number.startswith("4"):
                return CreditCardIssuer.VISA
            if 51 <= int(card_number[:2]) <= 55:
                return CreditCardIssuer.MASTERCARD
            return CreditCardIssuer.UNKNOWN
