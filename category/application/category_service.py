from category.domain.repository.category_repo import ICategoryRepository
from dependency_injector.wiring import inject


class CategoryService:
    @inject
    def __init__(self, category_repo: ICategoryRepository):
        self.repository = category_repo

    def create_category(self, category):
        return self.repository.create_category(category)

    def get_category(self, category_id):
        return self.repository.get_category(category_id)

    def update_category(self, category):
        return self.repository.update_category(category)

    def delete_category(self, category_id):
        return self.repository.delete_category(category_id)
    
    def get_categories(self, page, items_per_page):
        return self.repository.get_categories(page, items_per_page)

