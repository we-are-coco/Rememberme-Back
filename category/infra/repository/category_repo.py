from category.domain.repository.category_repo import ICategoryRepository
from category.infra.db_models.category import Category as CategoryModel
from category.domain.category import Category as CategoryVO
from database import SessionLocal
from datetime import datetime
from utils.db_utils import row_to_dict
from sqlalchemy.orm import noload


class CategoryRepository(ICategoryRepository):

    def create_category(self, category):
        with SessionLocal() as db:
            db_category = CategoryModel(**category.__dict__)
            db.add(db_category)
            db.commit()
            db.refresh(db_category)
            return db_category
        return None

    def get_category(self, category_id):
        with SessionLocal() as db:
            return db.query(CategoryModel).filter(CategoryModel.id == category_id).first()

    def update_category(self, category):
        with SessionLocal() as db:
            db_category = db.query(CategoryModel).filter(CategoryModel.id == category.id).first()
            if db_category:
                db_category.name = category.name
                db_category.updated_at = datetime.now()
                db.commit()
                db.refresh(db_category)
                return db_category
        return None

    def delete_category(self, category_id):
        with SessionLocal() as db:
            db_category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
            if db_category:
                db.delete(db_category)
                db.commit()
                return db_category
        return None

    def get_categories(self, page, items_per_page):
        with SessionLocal() as db:
            query = db.query(CategoryModel)
            total_count = query.count()
            categories = query.offset((page-1) * items_per_page).limit(items_per_page).all()
            return total_count, categories
        return None