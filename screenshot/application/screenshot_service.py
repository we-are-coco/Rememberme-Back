from screenshot.domain.repository.screenshot_repo import IScreenshotRepository
from category.domain.repository.category_repo import ICategoryRepository
from notification.domain.repository.notification_repo import INotificationRepository
from screenshot.domain.screenshot import Screenshot
from category.domain.category import Category
from notification.domain.notification import Notification
from ulid import ULID
from dependency_injector.wiring import inject
from datetime import datetime
from utils.ai import AImodule
from screenshot.infra.storage.azure_blob import AzureBlobStorage
import os
from utils.logger import logger


class ScreenshotService:
    @inject
    def __init__(self,
                screenshot_repo: IScreenshotRepository, 
                ai_module: AImodule,
                category_repo: ICategoryRepository,
                notification_repo: INotificationRepository,
            ):
        self.screenshot_repo = screenshot_repo
        self.category_repo = category_repo
        self.notification_repo = notification_repo
        self.ai_module = ai_module
        self.storage = AzureBlobStorage()
        self.ulid = ULID()

    def get_screenshots(
            self,
            user_id: str,
            page: int,
            items_per_page: int,
            search_text: str,
    ) -> tuple[int, list[Screenshot]]:
        # todo: extract keyword
        # keywords = self.ai_module.extract_keywords(search_text)
        #keywords = ["신세계", "상품권", "30000원"]
        return self.screenshot_repo.get_screenshots(user_id, page, items_per_page, search_text)
    
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
            brand: str,
            type: str,
            date: str,
            time: str,
            from_location: str,
            to_location: str,
            location: str,
            details: str,
            notifications: list[datetime],
    ) -> Screenshot:
        screenshot_id = self.ulid.generate()
        notification_vos = []
        category = self.category_repo.get_category(category_id)
        for notification in notifications:
            notification_vos.append(Notification(
                id=self.ulid.generate(),
                user_id=user_id,
                screenshot_id=screenshot_id,
                notification_time=notification,
                is_sent=False,
                message=f"{category.name} 알림 {notification.strftime('%Y-%m-%d %H:%M')}",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        screenshot = Screenshot(
            id=screenshot_id,
            title=title,
            description=description,
            category_id=category_id,
            url=url,
            start_date=start_date,
            end_date=end_date,
            price=price,
            code=code,
            user_id=user_id,
            brand=brand,
            type=type,
            date=date,
            time=time,
            from_location=from_location,
            to_location=to_location,
            location=location,
            details=details,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        self.screenshot_repo.save(user_id, screenshot)
        self.notification_repo.save_all(notification_vos)
        return screenshot
    
    def update_screenshot(
            self,
            user_id: str,
            screenshot_id: str,
            url: str | None = None,
            title: str | None = None,
            price: float | None = None,
            code: str | None = None,
            description: str | None = None,
            category_id: str | None = None,
            brand: str | None = None,
            type: str | None = None,
            date: str | None = None,
            time: str | None = None,
            from_location: str | None = None,
            to_location: str | None = None,
            location: str | None = None,
            details: str | None = None,
            start_date: datetime | None = None,
            end_date: datetime | None = None
    ) -> Screenshot:
        screenshot = self.screenshot_repo.find_by_id(user_id, screenshot_id)
        screenshot.title = title or screenshot.title
        screenshot.description = description or screenshot.description
        screenshot.category_id = category_id or screenshot.category_id
        screenshot.url = url or screenshot.url
        screenshot.price = price or screenshot.price
        screenshot.code = code or screenshot.code
        screenshot.brand = brand or screenshot.brand
        screenshot.type = type or screenshot.type
        screenshot.date = date or screenshot.date
        screenshot.time = time or screenshot.time
        screenshot.from_location = from_location or screenshot.from_location
        screenshot.to_location = to_location or screenshot.to_location
        screenshot.location = location or screenshot.location
        screenshot.details = details or screenshot.details
        screenshot.start_date = start_date or screenshot.start_date
        screenshot.end_date = end_date or screenshot.end_date

        self.screenshot_repo.update(user_id, screenshot)
        return screenshot
    
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
            file_path: str,
    ) -> Screenshot:
        url = self.storage.upload_image(file_path, f'{user_id}/{file_path}')
        analyze_result = self.ai_module.analyze_image(file_path)

        try:
            os.remove(file_path)
        except Exception as e:
            logger.error(f"Failed to remove file: {file_path}")

        category = self.category_repo.find_by_name(analyze_result.get("category", None))

        screenshot = Screenshot(
            id=None,
            title=analyze_result.get("title", None),
            description=analyze_result.get("description", None),
            category_id=category.id if category else None,
            url=url,
            start_date=analyze_result.get("start_date", None),
            end_date=analyze_result.get("end_date", None),
            price=analyze_result.get("price", None),
            code=analyze_result.get("code", None),
            brand=analyze_result.get("brand", None),
            type=analyze_result.get("type", None),
            date=analyze_result.get("date", None),
            time=analyze_result.get("time", None),
            from_location=analyze_result.get("from_location", None),
            to_location=analyze_result.get("to_location", None),
            location=analyze_result.get("location", None),
            details=analyze_result.get("details", None),
            user_id=user_id,
            created_at=None,
            updated_at=None,
        )
        return screenshot
        