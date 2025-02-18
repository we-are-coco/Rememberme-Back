import pytest
from user.application.user_service import UserService
from user.infra.repository.user_repo import UserRepository
from user.domain.user import User
from screenshot.domain.screenshot import Screenshot
from notification.domain.notification import Notification


@pytest.fixture
def user_repo():
    return UserRepository()

@pytest.fixture
def user_service(user_repo):
    return UserService(user_repo=user_repo)


@pytest.fixture
def get_test_user(user_service):
    try:
        user = user_service.get_user_by_email("testuser@example.com")
        yield user
    except Exception as e:
        user = user_service.create_user(
            name="testuser",
            email="testuser@example.com",
            password="password123"
        )
        yield user

    user_service.delete_user(user.id)


def test_create_user(user_service):
    # Create a new user
    user = user_service.create_user(
        name="testuser",
        email="testuser@example.com",
        password="password123"
    )
    
    # Assert that the user was created successfully
    assert isinstance(user, User)
    assert user.name == "testuser"
    assert user.email == "testuser@example.com"
    assert user.password is not None  # Password hash should be set after hashing

    # Clean up: Delete the user from the repository
    user_service.delete_user(user.id)


def test_update_user(get_test_user, user_service):
    # Update an existing user
    user = get_test_user

    user = user_service.update_user(user.id, name="updatedtestuser", fcm_token="new_fcm_token")

    # Assert that the user was updated successfully
    assert isinstance(user, User)
    assert user.name == "updatedtestuser"
    assert user.fcm_token == "new_fcm_token"


def test_find_by_email(get_test_user, user_service):
    # Find a user by email
    user = get_test_user

    found_user = user_service.get_user_by_email(user.email)

    # Assert that the correct user was found
    assert isinstance(found_user, User)
    assert found_user.id == user.id
