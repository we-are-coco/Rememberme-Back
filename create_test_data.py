
from user.application.user_service import UserService
from notification.application.notification_service import NotificationService
from screenshot.application.screenshot_service import ScreenshotService
from category.application.category_service import CategoryService
from user.infra.repository.user_repo import UserRepository
from notification.infra.repository.notification_repo import NotificationRepository
from screenshot.infra.repository.screenshot_repo import ScreenshotRepository
from category.infra.repository.category_repo import CategoryRepository
from utils import ai
from datetime import datetime, timedelta


def create_test_user(user_service: UserService):
    try:
        user = user_service.create_user(
            name="mingi",
            email="pangshe10@gmail.com",
            password="test-password",
        )
    except Exception as e:
        user = user_service.get_user_by_email("pangshe10@gmail.com")
    return user

def create_test_category(category_service: CategoryService, category_names: list[str]):
    res = []
    for name in category_names:
        try:
            category = category_service.create_category(name=name)
        except Exception as e:
            category = category_service.get_category_by_name(name)
        res.append(category)
    return res

def create_test_data():
    ai_module = ai.AImodule()
    user_repo = UserRepository()
    notification_repo = NotificationRepository()
    screenshot_repo = ScreenshotRepository()
    category_repo = CategoryRepository()

    user_service = UserService(user_repo)
    notification_service = NotificationService(notification_repo)
    category_service = CategoryService(category_repo)
    screenshot_service = ScreenshotService(
        category_repo=category_repo, 
        screenshot_repo=screenshot_repo,
        notification_repo=notification_repo,
        ai_module=ai_module,
    )

    user = create_test_user(user_service)

    category_names = ["쿠폰", "엔터테인먼트", "교통", "약속", "불명"]
    category_coupon = create_test_category(category_service, category_names)[0]

    notifications = [
        datetime.astimezone(datetime.now() + timedelta(days=1)),
        datetime.astimezone(datetime.now() + timedelta(days=2)),
        datetime.astimezone(datetime.now() + timedelta(days=3)),
    ]

    for i in range(5):
        screenshot_service.create_screenshot(
            user_id=user.id,
            title=f"신세계이마트 30,000원 상품권 {i}",
            category_id=category_coupon.id,
            description="신세계이마트에서 사용 가능한 30,000원 상품권",
            url="http://example.com/test.png",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=5 + i),
            price=1000,
            code="1023-8167-1826",
            brand="신세계이마트",
            type="상품권",
            date=datetime.strftime(datetime.now() + timedelta(days=9) - timedelta(days=1) * i, "%Y-%m-%d"),
            time=datetime.strftime(datetime.now() + timedelta(hours=3) - timedelta(hours=1) * i, "%H:%M"),
            from_location="test_from_location",
            to_location="test_to_location",
            location="test_location",   
            details="test_details",
            notifications=notifications,
        )


create_test_data()