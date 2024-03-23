from pymongo.collection import Collection
from pymongo.database import Database
from app.models.models import Category,PyObjectId
from typing import List, Union
from bson import ObjectId

class CategoryRepository:
    def __init__(self, db: Database) -> None:
        self.db: Database = db
        self.categories: Collection = self.db['categories']
    
    def get_categories(self) -> List[Category]:
        return list(self.categories.find({}))
    
    def get_category_by_id(self, id:PyObjectId) -> Union[Category,None]: 
        category:Union[Category,None] = self.categories.find_one({"_id": ObjectId(id)})
        if not category:
            return None
        return Category(**category)


    def get_category_by_name(self, category_name: str) -> Union[Category, None]:
        category_data:Union[Category, None] = self.categories.find_one({"name": {"$regex": f"^{category_name}$", "$options": "i"}})

        if not category_data:
            return None
                
        return Category(**category_data)

    

     
            
       
