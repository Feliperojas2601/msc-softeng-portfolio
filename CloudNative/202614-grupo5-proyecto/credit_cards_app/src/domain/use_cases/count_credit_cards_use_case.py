from domain.ports.credit_card_repository_port import CreditCardRepositoryPort


class CountCreditCardsUseCase:
    def __init__(self, repository: CreditCardRepositoryPort):
        self.repository = repository

    def execute(self) -> int:
        return self.repository.count()
