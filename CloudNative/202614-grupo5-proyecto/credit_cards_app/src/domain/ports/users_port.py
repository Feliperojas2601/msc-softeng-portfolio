from abc import ABC, abstractmethod


class UsersPort(ABC):
    @abstractmethod
    def get_user_id(self, token: str) -> str:
        raise NotImplementedError
