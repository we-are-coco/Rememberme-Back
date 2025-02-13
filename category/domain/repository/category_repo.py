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
    
    @abstractmethod
    def find_by_name(self, category_name):
        raise NotImplementedError