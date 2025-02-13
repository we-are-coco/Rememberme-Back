from abc import ABCMeta
from abc import abstractmethod
from user.domain.user import User


class IUserRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, user: User) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_email(self, email: str) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_id(self, user_id: int) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_users(self, page: int, items_per_page: int) -> tuple[int, list[User]]:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, user_id: int) -> None:
        raise NotImplementedError