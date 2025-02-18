import pytest

from notification.domain.notification import Notification
from user.application.user_service import UserService
from user.infra.repository.user_repo import UserRepository
from screenshot.infra.repository.screenshot_repo import ScreenshotRepository
from screenshot.application.screenshot_service import ScreenshotService
from category.application.category_service import CategoryService
from category.infra.repository.category_repo import CategoryRepository
from screenshot.domain.screenshot import Screenshot
from notification.infra.repository.notification_repo import NotificationRepository
from notification.application.notification_service import NotificationService
from datetime import datetime, timedelta
from utils import ai


@pytest.fixture
def category_repo():
    return CategoryRepository()

@pytest.fixture
def notification_repo():
    return NotificationRepository()

@pytest.fixture
def aimodule():
    return ai.AImodule()

@pytest.fixture
def user_service():
    return UserService(user_repo=UserRepository())

@pytest.fixture
def category_service(category_repo):
    return CategoryService(category_repo=category_repo)


@pytest.fixture
def testcategory(category_service):
    category = category_service.create_category("testcategoryname")
    yield category
    category_service.delete_category(category_id=category.id)

@pytest.fixture
def screenshot_service(notification_repo, aimodule, category_repo):
    return ScreenshotService(
        screenshot_repo=ScreenshotRepository(),
        ai_module=aimodule, 
        notification_repo=notification_repo, 
        category_repo=category_repo
    )


@pytest.fixture
def testuser(user_service):
    user = user_service.create_user("testuser", "testuser@example.com", "password123")
    yield user
    user_service.delete_user(user.id)


@pytest.fixture
def testscreenshot(testuser, testcategory, screenshot_service):
    user = testuser
    category = testcategory

    notification_vos = [
        datetime.now(),
        datetime.now() + timedelta(hours=1)
    ]

    screenshot = screenshot_service.create_screenshot(
        user_id=user.id,
        title="testtitle",
        description="testdescription",
        url="https://example.com/test.jpg",
        category_id=category.id,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=1),
        price=100.0,
        code="testcode",
        brand="testbrand",
        type="testtype",
        date="2025-04-01",
        time="12:00",
        from_location="testfromlocation",
        to_location="testtolocation",
        location="testlocation",
        details="testdetails",
        notifications=notification_vos
    )

    yield screenshot
    screenshot_service.delete_screenshot(user.id, screenshot.id)


@pytest.fixture
def notification_service(notification_repo):
    return NotificationService(notification_repo=notification_repo)


def test_find_notification(testuser, testscreenshot, notification_service):
    user = testuser
    notifications = notification_service.get_notifications(user.id, 1, 10)
    assert len(notifications) == 2