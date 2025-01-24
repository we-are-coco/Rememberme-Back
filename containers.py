from dependency_injector import containers, providers
from user.infra.repository.user_repo import UserRepository
from screenshot.infra.repository.screenshot_repo import ScreenshotRepository
from user.application.user_service import UserService
from screenshot.application.screenshot_service import ScreenshotService



class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["user", "screenshot"],
    )

    user_repo = providers.Factory(UserRepository)
    user_service = providers.Factory(UserService, user_repo=user_repo)

    screenshot_repo = providers.Factory(ScreenshotRepository)
    screenshot_service = providers.Factory(ScreenshotService, screenshot_repo=screenshot_repo)
    
