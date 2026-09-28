from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PaymentTokenizationResult:
    token: str
    issuer: str
    ruv: str | None


class PaymentProviderPort(ABC):
    @abstractmethod
    def tokenize(
        self,
        *,
        card_number: str,
        cvv: str,
        expiration_date: str,
        card_holder_name: str,
    ) -> PaymentTokenizationResult:
        raise NotImplementedError
