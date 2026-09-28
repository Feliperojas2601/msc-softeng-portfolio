from domain.models.credit_card import CreditCardStatus
from domain.ports.credit_card_repository_port import CreditCardRepositoryPort
from errors import CreditCardNotFoundError


class FinalizeCreditCardVerificationUseCase:
    def __init__(self, repository: CreditCardRepositoryPort):
        self.repository = repository

    def execute(self, card_id: str, status: str):
        try:
            normalized_status = CreditCardStatus(status)
        except ValueError:
            raise ValueError("invalid verification status") from None
        if normalized_status == CreditCardStatus.POR_VERIFICAR:
            raise ValueError("verification status must be terminal")
        card = self.repository.finalize_verification(card_id, normalized_status.value)
        if card is None:
            raise CreditCardNotFoundError()
        return card
