from fastapi import UploadFile
from screenshot.domain.repository.screenshot_repo import IScreenshotRepository
from screenshot.domain.screenshot import Screenshot, Category
from ulid import ULID
from dependency_injector.wiring import inject
from datetime import datetime
from utils.ai import AImodule


class ScreenshotService:
    @inject
    def __init__(self, screenshot_repo: IScreenshotRepository, ai_module: AImodule):
        self.screenshot_repo = screenshot_repo
        self.ai_module = ai_module
        self.ulid = ULID()

    def get_screenshots(
            self,
            user_id: str,
            page: int,
            items_per_page: int
    ) -> tuple[int, list[Screenshot]]:
        return self.screenshot_repo.get_screenshots(user_id, page, items_per_page)
    
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
            category_id: str,
            description: str,
            url: str,
            start_date: datetime,
            end_date: datetime,
            price: float,
            code: str,
    ) -> Screenshot:
        screenshot = Screenshot(
            id=self.ulid.generate(),
            title=title,
            description=description,
            category_id=category_id,
            url=url,
            start_date=start_date,
            end_date=end_date,
            price=price,
            code=code,
            user_id=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        self.screenshot_repo.save(user_id, screenshot)
        return screenshot
    
    def update_screenshot(
            self,
            user_id: str,
            screenshot_id: str,
            image: str | None = None,
            title: str | None = None,
            price: float | None = None,
            code: str | None = None,
            description: str | None = None,
            category_id: str | None = None,
    ) -> Screenshot:
        screenshot = self.screenshot_repo.find_by_id(user_id, screenshot_id)
        if title:
            screenshot.title = title
        if description:
            screenshot.description = description
        if category_id:
            screenshot.category_id = category_id
        if image:
            screenshot.url = image
        if price:
            screenshot.price = price
        if code:
            screenshot.code = code
        
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
            category_name: str,
            page: int,
            items_per_page: int
    ) -> tuple[int, list[Screenshot]]:
        return self.screenshot_repo.get_screenshot_by_category(
            user_id, 
            category_name, 
            page,
            items_per_page
        )
    
    def upload_screenshot_image(
            self,
            user_id: str,
            file: UploadFile
    ) -> Screenshot:
        url = self.screenshot_repo.upload_screenshot_image(user_id, file)
        analyze_result = self.ai_module.analyze_image(file.file)

        screenshot = Screenshot(
            id=None,
            title=analyze_result.get("type", None),
            description=analyze_result.get("description", None),
            category_id=analyze_result.get("category", None),
            url=url,
            start_date=analyze_result.get("start_date", None),
            end_date=analyze_result.get("end_date", None),
            price=analyze_result.get("price", None),
            code=analyze_result.get("code", None),
            user_id=user_id,
            created_at=None,
            updated_at=None,
        )
        return screenshot
        