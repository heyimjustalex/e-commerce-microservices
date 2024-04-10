from typing import Any, Dict, Union, List
from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertOneResult
from pymongo.client_session import ClientSession
from pymongo.results import InsertOneResult, UpdateResult

from app.models.models import ProductStub,PyObjectId

class ProductRepository:
    def __init__(self, db: Database, client:MongoClient) -> None:
        self.db: Database = db
        self.products: Collection = self.db['products']
        self.client:MongoClient = client

    def create_product(self, product: ProductStub) -> ProductStub:
        product_dict: Dict[str, Any] = product.model_dump()
        retrived_id : str = product.id
  
        if retrived_id:
            product_dict['_id'] = retrived_id
            
        insert_result: InsertOneResult = self.products.insert_one(product_dict)
        product.id = str(insert_result.inserted_id)
        return product
    
    def get_mongo_client(self)-> MongoClient:
        return self.client
    
    def get_products(self) -> List[ProductStub]:
        products_data = list(self.products.find({}))  
        products: List[ProductStub] = [ProductStub(**data) for data in products_data]  
        return products    

    def get_product_by_name(self,name:str) -> Union[ProductStub, None]:
        product: Union[ProductStub, None]  = self.products.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
        if not product:
            return None
        return ProductStub(**product)
    
    def update_product_quantity_by_name(self, name: str, new_number: int, session: ClientSession) -> ProductStub | None:
        
        update_result: UpdateResult = self.products.update_one(
            {"name": name.lower()},
            {"$set": {"quantity": new_number}},
            session=session
        )   

        if update_result.matched_count == 1:
            product: Union[ProductStub, None]  = self.products.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
            if not product:
                return None
            return ProductStub(**product)
        return None           
        
    def get_products_of_category(self, category_id:PyObjectId) -> Union[List[ProductStub], None]:
        products_data = list(self.products.find({"categories": ObjectId(category_id)}))
        if not products_data:
            return None
        products: List[ProductStub] = [ProductStub(**data) for data in products_data]
        return products

     
            
       
