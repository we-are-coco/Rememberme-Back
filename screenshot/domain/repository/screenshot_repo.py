from abc import ABC, abstractmethod

from screenshot.domain.screenshot import Screenshot
from category.domain.category import Category

class IScreenshotRepository(ABC):
    @abstractmethod
    def get_screenshots(self, screenshot_id: str, page: int, items_per_page: int, keywords: list[str]) -> tuple[int, list[Screenshot]]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, user_id: str, screenshot_id: str) -> Screenshot:
        raise NotImplementedError
    
    @abstractmethod
    def save(self, user_id: str, screenshot: Screenshot) -> Screenshot:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, user_id: str, screenshot: Screenshot) -> Screenshot:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, user_id: str, screenshot_id: str):
        raise NotImplementedError
    
    @abstractmethod
    def get_screenshot_by_category(
        self, 
        user_id: str, 
        category: str,
        page: int,
        items_per_page: int
    ) -> tuple[int, list[Screenshot]]:
        raise NotImplementedError

    @abstractmethod
    def find_category_by_name(self, category_name: str) -> list[Category]:
        raise NotImplementedError