from pymongo.collection import Collection
from pymongo.database import Database
from typing import List, Union
from bson import ObjectId

from app.models.models import Category,PyObjectId

class CategoryRepository:
    def __init__(self, db: Database) -> None:
        self.db: Database = db
        self.categories: Collection = self.db['categories']
    
    def get_categories(self) -> List[Category]:
        categories_data= self.categories.find({})
        categories : List[Category] = [Category(**data) for data in categories_data]
        return categories
    def get_category_by_id(self, id:PyObjectId) -> Union[Category,None]: 
        category:Union[Category,None] = self.categories.find_one({"_id": ObjectId(id)})
        if not category:
            return None
        return 

    def get_category_by_name(self, category_name: str) -> Union[Category, None]:
        category_data:Union[Category, None] = self.categories.find_one({"name": {"$regex": f"^{category_name}$", "$options": "i"}})

        if not category_data:
            return None                
        return Category(**category_data)

    

     
            
       
