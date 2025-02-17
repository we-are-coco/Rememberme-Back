from notification.domain.repository.notification_repo import INotificationRepository
from datetime import datetime
from notification.domain.notification import Notification
from ulid import ULID
from dependency_injector.wiring import inject
from fastapi.exceptions import HTTPException


class NotificationService:
    @inject
    def __init__(self, notification_repo: INotificationRepository):
        self.repo = notification_repo
        self.ulid = ULID()

    def create_notification(self, user_id: str, screenshot_id: str, notification_time: datetime, message: str):
        """ 특정 스크린샷에 대한 알림 생성 """
        notification = Notification(
            id=self.ulid.generate(),
            user_id=user_id,
            screenshot_id=screenshot_id,
            notification_time=notification_time,
            message=message,
            is_sent=False,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.repo.save(user_id, notification)
        return notification

    def get_notifications(self, user_id: str, page: int, items_per_page: int):
        """ 사용자의 모든 알림 조회 (페이징) """
        return self.repo.get_notifications(user_id, page, items_per_page)

    def get_notification(self, user_id: str, notification_id: str):
        """ 특정 알림 조회 """
        notification = self.repo.find_by_id(user_id, notification_id)
        if not notification:
            raise HTTPException(status_code=422, detail="Notification not found")

    def delete_notification(self, user_id: str, notification_id: str):
        """ 특정 알림 삭제 """
        self.repo.delete(user_id, notification_id)

    def mark_notification_as_sent(self, user_id: str, notification_id: str):
        """ 특정 알림을 '보낸 상태'로 변경 """
        return self.repo.mark_notification_as_sent(user_id, notification_id)

    def get_pending_notifications(self):
        """ 전송되지 않은 알림 조회 """
        return self.repo.get_pending_notifications()