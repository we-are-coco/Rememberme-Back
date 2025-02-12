from abc import ABCMeta, abstractmethod

class ICategoryRepository(metaclass=ABCMeta):

    @abstractmethod
    def create_category(self, category):
        raise NotImplementedError

    @abstractmethod
    def get_category(self, category_id):
        raise NotImplementedError

    @abstractmethod
    def update_category(self, category):
        raise NotImplementedError

    @abstractmethod
    def delete_category(self, category_id):
        raise NotImplementedError

    @abstractmethod
    def get_categories(self, page, items_per_page):
        raise NotImplementedError