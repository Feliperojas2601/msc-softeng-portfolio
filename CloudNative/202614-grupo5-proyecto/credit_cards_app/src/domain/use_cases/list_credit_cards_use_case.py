from domain.models.credit_card import CreditCard
from domain.ports.credit_card_repository_port import CreditCardRepositoryPort
from domain.ports.users_port import UsersPort


class ListCreditCardsUseCase:
    def __init__(self, repository: CreditCardRepositoryPort, users: UsersPort):
        self.repository = repository
        self.users = users

    def execute(self, token: str) -> list[CreditCard]:
        user_id = self.users.get_user_id(token)
        return self.repository.list_by_user(user_id)
