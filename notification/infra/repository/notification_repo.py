from sqlalchemy.orm import Session
from sqlalchemy import or_
from notification.infra.db_models.notification import Notification
from notification.domain.repository.notification_repo import INotificationRepository
from notification.domain.notification import Notification as NotificationVO
from user.infra.db_models.user import User
from utils.db_utils import row_to_dict
import uuid
from datetime import datetime
from database import SessionLocal
from utils.common import get_time_description
from screenshot.infra.db_models.screenshot import Screenshot



class NotificationRepository(INotificationRepository):  
    def save(self, user_id: str, notification_vo: NotificationVO) -> Notification:
        """ 특정 스크린샷에 대한 알림 생성 """
        with SessionLocal() as db:
            notification = Notification(
                id=notification_vo.id,
                user_id=user_id,
                screenshot_id=notification_vo.screenshot_id,
                notification_time=notification_vo.notification_time,
                is_sent=notification_vo.is_sent,
                message=notification_vo.message,
            )
            db.add(notification)
            db.commit()
            db.refresh(notification)
            

    def get_notifications(self, user_id: str, page: int, items_per_page: int):
        """ 사용자의 모든 알림 조회 (페이징) """
        with SessionLocal() as db:
            query = (
                db.query(Notification)
                .filter(Notification.user_id == user_id)
                .join(Screenshot, Notification.screenshot_id == Screenshot.id)
            )

            total_count = query.count()
            notifications = (
                query.order_by(Notification.notification_time.asc())
                .offset((page - 1) * items_per_page)
                .limit(items_per_page)
                .all()
            )

            notification_vos = []
            for notification in notifications:
                noti = row_to_dict(notification)
                noti['time_description'] = get_time_description(notification.notification_time)
                notification_vos.append(NotificationVO(**noti))

            return total_count, notification_vos

    def find_by_id(self, user_id: str, notification_id: str) -> dict:
        """ 특정 알림 조회 """
        with SessionLocal() as db:
            notification = db.query(Notification).filter(
                Notification.id == notification_id,
                Notification.user_id == user_id
            ).first()

            if notification:
                notification_vo = row_to_dict(notification)
                notification_vo['time_description'] = get_time_description(notification.notification_time)
                return NotificationVO(**notification_vo)
            return None
        
    def update(self, user_id: str, notification_vo: NotificationVO) -> Notification:
        """ 특정 알림 업데이트 """
        with SessionLocal() as db:
            notification = db.query(Notification).filter(
                Notification.id == notification_vo.id,
                Notification.user_id == user_id
            ).first()

            if notification:
                notification.notification_time = notification_vo.notification_time
                notification.message = notification_vo.message
                notification.is_sent = notification_vo.is_sent
                notification.updated_at = datetime.now()
                db.commit()
                db.refresh(notification)
                notification_vo = row_to_dict(notification)
                notification_vo['time_description'] = get_time_description(notification.notification_time)
                return NotificationVO(**notification_vo)
            return None

    def delete(self, user_id: str, notification_id: str):
        """ 특정 알림 삭제 """
        with SessionLocal() as db:
            notification = db.query(Notification).filter(
                Notification.id == notification_id,
                Notification.user_id == user_id
            ).first()

            if notification:
                db.delete(notification)
                db.commit()

    def delete_all(self, user_id: str, screenshot_id: str):
        """ 사용자의 모든 알림 삭제 """
        with SessionLocal() as db:
            db.query(Notification).filter(
                Notification.user_id == user_id,
                Notification.screenshot_id == screenshot_id,
            ).delete()
            db.commit()

    def mark_notification_as_sent(self, user_id: str, notification_id: str) -> NotificationVO:
        """ 특정 알림을 '보낸 상태'로 변경 """
        with SessionLocal() as db:
            notification = db.query(Notification).filter(
                Notification.id == notification_id,
                Notification.user_id == user_id
            ).first()

            if notification:
                notification.is_sent = True
                notification.updated_at = datetime.now()
                db.commit()
                db.refresh(notification)
                noti_dict = row_to_dict(notification)
                noti_dict['time_description'] = get_time_description(notification.notification_time)
                return NotificationVO(**noti_dict)

            return None

    def get_pending_notifications(self):
        """ 전송되지 않은 알림 조회 (현재 시각을 기준) """
        with SessionLocal() as db:
            return (
                db.query(Notification, User.fcm_token)
                    .join(User, Notification.user_id == User.id)
                    .filter(
                        Notification.is_sent == False,
                        Notification.notification_time <= datetime.now()
                ).all()
            )
        
    def save_all(self, notification_vos: list[NotificationVO]):
        """ 여러 알림 생성 """
        with SessionLocal() as db:
            notifications = [
                Notification(
                    id=notification_vo.id,
                    user_id=notification_vo.user_id,
                    screenshot_id=notification_vo.screenshot_id,
                    notification_time=notification_vo.notification_time,
                    is_sent=notification_vo.is_sent,
                    message=notification_vo.message,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
                for notification_vo in notification_vos
            ]
            db.add_all(notifications)
            db.commit()
            noti_vos = []
            for notification in notifications:
                noti_dict = row_to_dict(notification)
                noti_dict["time_description"] = get_time_description(notification.notification_time)
                noti_vo = NotificationVO(**noti_dict)
                noti_vos.append(noti_vo)

            return noti_vos