import pytest

from user.infra.repository.user_repo import UserRepository
from notification.infra.db_models.notification import Notification
from screenshot.infra.db_models.screenshot import Screenshot
from category.application.category_service import CategoryService
from category.infra.repository.category_repo import CategoryRepository
from database import engine, Base


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def category_repository():
    return CategoryRepository()

@pytest.fixture
def category_service():
    return CategoryService(category_repo=category_repository())


def test_create_category(category_service):
    created_category = category_service.create_category("Test Category")
    assert created_category.name == "Test Category"

    # teardown
    category_service.delete_category(created_category.id)