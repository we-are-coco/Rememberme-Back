from category.domain.repository.category_repo import ICategoryRepository
from dependency_injector.wiring import inject
from category.domain.category import Category
from ulid import ULID
from datetime import datetime


class CategoryService:
    @inject
    def __init__(self, category_repo: ICategoryRepository):
        self.repository = category_repo
        self.ulid = ULID()

    def create_category(self, name: str):
        category = Category(
            id=self.ulid.generate(),
            name=name,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            screenshot=[],
        )
        return self.repository.create_category(category)

    def get_category(self, category_id):
        return self.repository.get_category(category_id)

    def update_category(self, category):
        return self.repository.update_category(category)

    def delete_category(self, category_id):
        return self.repository.delete_category(category_id)
    
    def get_categories(self, page, items_per_page):
        return self.repository.get_categories(page, items_per_page)

