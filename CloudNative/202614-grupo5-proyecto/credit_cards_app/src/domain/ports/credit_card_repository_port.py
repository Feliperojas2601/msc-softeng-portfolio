from abc import ABC, abstractmethod

from domain.models.credit_card import CreditCard


class CreditCardRepositoryPort(ABC):
    @abstractmethod
    def get_by_id(self, card_id: str) -> CreditCard | None:
        raise NotImplementedError

    @abstractmethod
    def create(self, credit_card: CreditCard) -> CreditCard:
        raise NotImplementedError

    @abstractmethod
    def exists_for_user(self, user_id: str, token: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def list_by_user(self, user_id: str) -> list[CreditCard]:
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def reset(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def finalize_verification(self, card_id: str, status: str) -> CreditCard | None:
        raise NotImplementedError
