from screenshot.domain.repository.screenshot_repo import IScreenshotRepository
from screenshot.domain.screenshot import Screenshot, Category
from ulid import ULID
from dependency_injector.wiring import inject
from datetime import datetime


class ScreenshotService:
    @inject
    def __init__(self, screenshot_repo: IScreenshotRepository):
        self.screenshot_repo = screenshot_repo
        self.ulid = ULID()

    def get_screenshots(
            self,
            screenshot_id: str,
            page: int,
            items_per_page: int
    ) -> tuple[int, list[Screenshot]]:
        return self.screenshot_repo.get_screenshots(screenshot_id, page, items_per_page)
    
    def get_screenshot(
            self,
            user_id: str,
            screenshot_id: str
    ) -> Screenshot:
        return self.screenshot_repo.find_by_id(user_id, screenshot_id)
    
    def create_screenshot(
            self,
            user_id: str,
            title: str,
            category: Category,
            description: str,
            url: str,
            start_date: datetime,
            end_date: datetime,
            price: float,
    ) -> Screenshot:
        screenshot = Screenshot(
            id=self.ulid.generate(),
            title=title,
            description=description,
            category=category,
            url=url,
            start_date=start_date,
            end_date=end_date,
            price=price,
            user_id=user_id,
        )
        return self.screenshot_repo.save(user_id, screenshot)
    
    def update_screenshot(
            self,
            user_id: str,
            screenshot_id: str,
            image: str | None = None,
            title: str | None = None,
            description: str | None = None,
            category: Category | None = None,
    ) -> Screenshot:
        screenshot = self.screenshot_repo.find_by_id(user_id, screenshot_id)
        if title:
            screenshot.title = title
        if description:
            screenshot.description = description
        if category:
            screenshot.category = category
        if image:
            screenshot.image = image
        
        return self.screenshot_repo.update(user_id, screenshot)
    
    def delete_screenshot(
            self,
            user_id: str,
            screenshot_id: str
    ):
        self.screenshot_repo.delete(user_id, screenshot_id)

    
    def get_screenshot_by_category(
            self,
            user_id: str,
            category: Category,
            page: int,
            items_per_page: int
    ) -> tuple[int, list[Screenshot]]:
        return self.screenshot_repo.get_screenshot_by_category(
            user_id, 
            category, 
            page,
            items_per_page
        )