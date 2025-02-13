from dependency_injector import containers, providers

from user.infra.repository.user_repo import UserRepository
from user.application.user_service import UserService
from screenshot.infra.repository.screenshot_repo import ScreenshotRepository
from screenshot.application.screenshot_service import ScreenshotService
from notification.infra.repository.notification_repo import NotificationRepository
from notification.application.notification_service import NotificationService
from category.infra.repository.category_repo import CategoryRepository
from category.application.category_service import CategoryService

from utils.ai import AImodule



class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["user", "screenshot", "notification", "category"],
    )

    user_repo = providers.Factory(UserRepository)
    user_service = providers.Factory(UserService, user_repo=user_repo)

    notification_repo = providers.Factory(NotificationRepository)
    notification_service = providers.Factory(NotificationService, notification_repo=notification_repo)

    category_repo = providers.Factory(CategoryRepository)
    category_service = providers.Factory(CategoryService, category_repo=category_repo)
    
    ai_module = providers.Factory(AImodule)
    screenshot_repo = providers.Factory(ScreenshotRepository)
    screenshot_service = providers.Factory(
        ScreenshotService,
        notification_repo=notification_repo,
        screenshot_repo=screenshot_repo,
        category_repo=category_repo,
        ai_module=ai_module
    )
