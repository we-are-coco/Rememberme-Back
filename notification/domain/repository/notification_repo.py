from abc import ABC, abstractmethod

from notification.domain.notification import Notification
from datetime import datetime


class INotificationRepository(ABC):
    @abstractmethod
    def save(self, user_id: str, screenshot_id: str, notification_time: datetime) -> Notification:
        raise NotImplementedError

    @abstractmethod
    def get_notifications(self, user_id: str, page: int, items_per_page: int):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, user_id: str, screenshot_id: str) -> Notification:
        raise NotImplementedError

    @abstractmethod
    def update(self, user_id: str, notification: Notification) -> Notification:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, user_id: str, screenshot_id: str):
        raise NotImplementedError

    @abstractmethod
    def mark_notification_as_sent(self, user_id: str, notification_id: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_pending_notifications(self):
        raise NotImplementedError
