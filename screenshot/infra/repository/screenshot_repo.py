from screenshot.domain.screenshot import Screenshot, Category
from screenshot.domain.repository.screenshot_repo import IScreenshotRepository
from sqlalchemy.orm import joinedload
from screenshot.domain.screenshot import Screenshot as ScreenshotVO
from database import SessionLocal
from utils.db_utils import row_to_dict
from fastapi import HTTPException


class ScreenshotRepository(IScreenshotRepository):

    def get_screenshots(
            self,
            screenshot_id, 
            page, 
            items_per_page
        ) -> tuple[int, list[Screenshot]]:
        with SessionLocal() as db:
            query = (
                db.query(Screenshot)
                .options(joinedload(Screenshot.category))
                .filter(Screenshot.id == screenshot_id)
            )

            total_count = query.count()
            screenshots = query.offset((page - 1) * items_per_page).limit(items_per_page).all()

            screenshot_vos = [ScreenshotVO(**row_to_dict(screenshot)) for screenshot in screenshots]
            return total_count, screenshot_vos

    
    def find_by_id(self, user_id: str, screenshot_id: str):
        with SessionLocal() as db:
            screenshot = (
                db.query(Screenshot)
                .options(joinedload(Screenshot.category))
                .filter(Screenshot.id == screenshot_id)
                .first()
            )
            if not screenshot:
                raise HTTPException(status_code=422, detail="Screenshot not found")
            return ScreenshotVO(**row_to_dict(screenshot))
    
    def save(self, user_id: str, screenshot_vo: ScreenshotVO) -> Screenshot:
        with SessionLocal() as db:
            category: Category = (
                db.query(Category)
                .filter(Category.id == screenshot_vo.category_id)
                .first()
            )
            screenshot = Screenshot(
                user_id=user_id,
                title=screenshot_vo.title,
                description=screenshot_vo.description,
                image=screenshot_vo.image,
                category=category
            )
            db.add(screenshot)
            db.commit()
            
    
    def update(self, user_id: str, screenshot_vo: ScreenshotVO) -> Screenshot:
        with SessionLocal() as db:
            screenshot = (
                db.query(Screenshot)
                .filter(Screenshot.id == screenshot_vo.id, user_id == screenshot_vo.user_id)
                .first()
            )
            if not screenshot:
                raise HTTPException(status_code=422, detail="Screenshot not found")
            
            screenshot.title = screenshot_vo.title
            screenshot.description = screenshot_vo.description
            screenshot.image = screenshot_vo.image
            screenshot.category = screenshot_vo.category
            db.add(screenshot)
            db.commit()
    
    def delete(self, user_id: str, screenshot_id: str):
        return super().delete(user_id, screenshot_id)
    
    def get_screenshot_by_category(
            self, 
            user_id: str, 
            category: Category, 
            page: int, 
            items_per_page: int
        ) -> tuple[int, list[Screenshot]]:
        return super().get_screenshot_by_category(user_id, category, page, items_per_page)