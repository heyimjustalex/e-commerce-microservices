from typing import List

from app.repositories.category_repository import CategoryRepository
from app.models.models import  Category

class CategoryService:
    def __init__(self,category_repository:CategoryRepository) -> None:
        self.category_repository:CategoryRepository = category_repository

    def get_categories(self) -> List[Category]:
        categories : List[Category] = self.category_repository.get_categories()
        return categories