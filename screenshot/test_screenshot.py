import pytest
from fastapi.testclient import TestClient
from main import app
from user.infra.repository.user_repo import UserRepository
from screenshot.infra.repository.screenshot_repo import ScreenshotRepository
from screenshot.application.screenshot_service import ScreenshotService
from category.infra.repository.category_repo import CategoryRepository
from category.application.category_service import CategoryService
from notification.application.notification_service import NotificationService
from notification.infra.repository.notification_repo import NotificationRepository
from user.application.user_service import UserService
from datetime import datetime, timedelta, timezone
from user.domain.user import User as UserVO
from notification.domain.notification import Notification as NotificationVO
from screenshot.domain.screenshot import Screenshot as ScreenshotVO
from utils import ai
from fastapi.exceptions import HTTPException
from user.domain.user import User
from database import Base, engine


client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def user_repo():
    return UserRepository()


@pytest.fixture
def user_service(user_repo):
    return UserService(user_repo)


@pytest.fixture
def get_user(user_service):
    try:
        user = user_service.create_user("testuser", "testuser@test.com", password="testuser123")
    except HTTPException as e:
        user = user_service.get_user_by_email("testuser@test.com")
    except Exception as e:
        raise e
    yield user
    user_service.delete_user(user.id)


@pytest.fixture
def screenshot_repo():
    return ScreenshotRepository()

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
def screenshot_service(screenshot_repo, category_repo, notification_repo, aimodule):
    return ScreenshotService(
        screenshot_repo=screenshot_repo, 
        category_repo=category_repo, 
        notification_repo=notification_repo, 
        ai_module=aimodule
    )

@pytest.fixture
def category_service(category_repo):
    return CategoryService(category_repo)


@pytest.fixture
def get_category(category_service):
    category = category_service.create_category("testcategoryname")
    yield category
    category_service.delete_category(category_id=category.id)

@pytest.fixture
def notification_repo():
    return NotificationRepository()

@pytest.fixture
def notification_service(notification_repo):
    return NotificationService(notification_repo)


def test_create_screenshot_기본(get_user, screenshot_service, get_category):
    user = get_user
    category = get_category

    screenshot = screenshot_service.create_screenshot(
        user_id=user.id, 
        title="testtitle", 
        category_id=category.id, 
        description="testdescription", 
        url="https://example.com/test.jpg", 
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
        notifications=[]
    )
    screenshot = screenshot_service.get_screenshot(user.id, screenshot.id)
    assert screenshot.title == "testtitle"
    assert screenshot.category_id == category.id
    assert screenshot.description == "testdescription"
    assert screenshot.url == "https://example.com/test.jpg"


def test_create_screenshot_with_notifications(get_user, get_category, screenshot_service, notification_service):
    user = get_user
    category = get_category

    notification_vos = [
        datetime.now(),
        datetime.now() + timedelta(days=1)
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

    screenshot = screenshot_service.get_screenshot(user.id, screenshot.id)
    assert screenshot.title == "testtitle"
    assert screenshot.description == "testdescription"
    assert screenshot.url == "https://example.com/test.jpg"
    assert screenshot.category_id == category.id

    notifications = notification_service.get_notifications(user_id=user.id, page=1, items_per_page=10)
    assert len(notifications) == 2


def test_create_screenshot_with_notification_and_delete_notification(get_user, get_category, screenshot_service, notification_service):
    user = get_user
    category = get_category

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

    screenshot = screenshot_service.get_screenshot(user.id, screenshot.id)
    assert screenshot.title == "testtitle"
    assert screenshot.description == "testdescription"
    assert screenshot.url == "https://example.com/test.jpg"
    assert screenshot.category_id == category.id

    count, notifications = notification_service.get_notifications(user_id=user.id, page=1, items_per_page=10)
    assert count == 2

    notification_service.delete_notification(user_id=user.id, notification_id=notifications[0].id)

    screenshot = screenshot_service.get_screenshot(user_id=user.id, screenshot_id=screenshot.id)
    assert screenshot.title == "testtitle"
    assert screenshot.description == "testdescription"
    assert screenshot.url == "https://example.com/test.jpg"
    assert screenshot.category_id == category.id


def test_set_is_used(get_user, get_category, screenshot_service, notification_service):
    user = get_user
    category = get_category

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

    screenshot = screenshot_service.set_used(user.id, screenshot.id)
    assert screenshot.is_used == True

    screenshot = screenshot_service.set_used(user.id, screenshot.id, False)
    assert screenshot.is_used == False
