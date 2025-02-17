from notification.application.notification_service import NotificationService
from notification.infra.repository.notification_repo import NotificationRepository
from fastapi_utilities import repeat_every

import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

cred = credentials.Certificate("rememberme_fcm.json")
firebase_admin.initialize_app(cred)


def send_push_notification(notification: dict):
    message = messaging.Message(
        notification=messaging.Notification(
            title="RememberMe 알림",
            body=notification.message
        ),
        token=notification.fcm_token
    )

    response = messaging.send(message)
    print("Successfully sent message:", response)


@repeat_every(seconds=300)
def check_and_send_notifications():
    print("🔔 Checking for pending notifications...")
    notification_repo = NotificationRepository()
    notification_service = NotificationService(notification_repo=notification_repo)
    pending_notifications = notification_service.get_pending_notifications()

    if pending_notifications:
        print(f"🔔 Found {len(pending_notifications)} pending notifications.")
    for notification in pending_notifications:
        # TODO: FCM 푸시 전송 로직 추가
        print(f"🔔 Sending notification to user {notification.user_id} for screenshot {notification.screenshot_id} at {notification.notification_time}")

        # 알림을 보낸 것으로 업데이트
        notification_service.mark_notification_as_sent(notification.id)

if __name__ == "__main__":
    check_and_send_notifications()