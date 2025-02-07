from screenshot.infra.db_models.screenshot import Screenshot, Category
from screenshot.domain.repository.screenshot_repo import IScreenshotRepository
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from screenshot.domain.screenshot import Screenshot as ScreenshotVO
from screenshot.domain.screenshot import Category as CategoryVO
from database import SessionLocal
from utils.db_utils import row_to_dict
from fastapi import HTTPException


class ScreenshotRepository(IScreenshotRepository):

    def get_screenshots(
            self,
            user_id, 
            page, 
            items_per_page,
            keywords: list[str],
        ) -> tuple[int, list[ScreenshotVO]]:
        with SessionLocal() as db:
            query = (
                db.query(Screenshot)
                .filter(Screenshot.user_id == user_id)
                .join(Category, Screenshot.category_id == Category.id)
                .options(joinedload(Screenshot.category))
            )
            if keywords:
                keyword_conditions = or_(
                    *[or_(
                        Screenshot.title.ilike(f"%{keyword}%"), 
                        Screenshot.description.ilike(f"%{keyword}%"), 
                        Category.name.ilike(f"%{keyword}%")
                    ) for keyword in keywords]
                )
                query = query.filter(keyword_conditions)

            total_count = query.count()
            screenshots = query.offset((page - 1) * items_per_page).limit(items_per_page).all()

            screenshot_vos = [ScreenshotVO(**row_to_dict(screenshot)) for screenshot in screenshots]
            return total_count, screenshot_vos

    
    def find_by_id(self, user_id: str, screenshot_id: str):
        with SessionLocal() as db:
            screenshot = (
                db.query(Screenshot)
                .filter(Screenshot.user_id == user_id, Screenshot.id == screenshot_id)
                .first()
            )
            if not screenshot:
                raise HTTPException(status_code=422, detail="Screenshot not found")
            return ScreenshotVO(**row_to_dict(screenshot))
    
    def save(self, user_id: str, screenshot_vo: ScreenshotVO):
        with SessionLocal() as db:
            category: Category = (
                db.query(Category)
                .filter(Category.id == screenshot_vo.category_id)
                .first()
            )
            screenshot = Screenshot(
                id=screenshot_vo.id,
                user_id=user_id,
                title=screenshot_vo.title,
                description=screenshot_vo.description,
                url=screenshot_vo.url,
                category_id=category.id,
                start_date=screenshot_vo.start_date,
                end_date=screenshot_vo.end_date,
                price=screenshot_vo.price,
                code=screenshot_vo.code,
            )
            db.add(screenshot)
            db.commit()
            
    
    def update(self, user_id: str, screenshot_vo: ScreenshotVO):
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
            screenshot.category_id = screenshot_vo.category_id
            screenshot.url = screenshot_vo.url
            screenshot.start_date = screenshot_vo.start_date
            screenshot.end_date = screenshot_vo.end_date
            screenshot.price = screenshot_vo.price
            screenshot.code = screenshot_vo.code
            db.add(screenshot)
            db.commit()
    
    def delete(self, user_id: str, screenshot_id: str):
        with SessionLocal() as db:
            screenshot = (
                db.query(Screenshot)
                .filter(Screenshot.id == screenshot_id, Screenshot.user_id == user_id)
                .first()
            )
            if not screenshot:
                raise HTTPException(status_code=422, detail="Screenshot not found")
            db.delete(screenshot)
            db.commit()
    
    def get_screenshot_by_category(
            self, 
            user_id: str, 
            category_name: str, 
            page: int, 
            items_per_page: int
        ) -> tuple[int, list[ScreenshotVO]]:
        with SessionLocal() as db:
            category = (
                db.query(Category)
                .filter(Category.name == category_name)
                .first()
            )
            if not category:
                raise HTTPException(status_code=422, detail="Category not found")
            query = (
                db.query(Screenshot)
                .filter(Screenshot.user_id == user_id, Screenshot.category_id == category.id)
            )
            total_count = query.count()
            screenshots = query.offset((page - 1) * items_per_page).limit(items_per_page).all()
            screenshot_vos = [ScreenshotVO(**row_to_dict(screenshot)) for screenshot in screenshots]
            return total_count, screenshot_vos

    def find_category_by_name(self, category_name: str) -> list[CategoryVO]:
        with SessionLocal() as db:
            category = (
                db.query(Category)
                .filter(Category.name == category_name)
                .first()
            )
            if not category:
                raise HTTPException(status_code=422, detail="Category not found")
            return CategoryVO(**row_to_dict(category))