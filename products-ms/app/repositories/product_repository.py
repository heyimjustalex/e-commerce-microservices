from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertOneResult, UpdateResult
from app.models.models import Product,PyObjectId
from typing import Any, Dict, Union
from typing import List
from pymongo import MongoClient
from pymongo.client_session import ClientSession
from bson import ObjectId

class ProductRepository:
    def __init__(self, db: Database, client:MongoClient) -> None:
        self.db: Database = db
        self.products: Collection = self.db['products']
        self.client:MongoClient = client

    def create_product(self, product: Product, session:None|ClientSession = None) -> Product:
        product_dict: Dict[str, Any] = product.model_dump(exclude_none=True)  
        row: InsertOneResult = self.products.insert_one(product_dict,session=session)
        product.id = str(row.inserted_id)
        return product
    
    def get_mongo_client(self)-> MongoClient:
        return self.client
    
    def get_products(self) -> List[Product]:
        products_data = list(self.products.find({}))  
        products: List[Product] = [Product(**data) for data in products_data]  
        return products    

    def get_product_by_name(self,name:str) -> Union[Product, None]:
        product: Union[Product, None]  = self.products.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
        if not product:
            return None
        return Product(**product)
    
    def decrease_product_quantity_by_name(self, name: str, decrease_number: int, session: ClientSession) -> Product | None:
        # Find the current quantity of the product
        current_product:Union[Product, None] =  self.products.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
        if current_product and current_product["quantity"] - decrease_number < 0:
           return None
        
        update_result: UpdateResult = self.products.update_one(
            {"name": name.lower()},
            {"$inc": {"quantity": -decrease_number}},
            session=session
        )   
        
        if update_result.matched_count == 1:
            product: Union[Product, None]  = self.products.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
            if not product:
                return None
            return Product(**product)
        return None
            
        
    def get_products_of_category(self, category_id:PyObjectId) -> Union[List[Product], None]:
        products_data = list(self.products.find({"categories": ObjectId(category_id)}))
        if not products_data:
            return None
        products: List[Product] = [Product(**data) for data in products_data]
        return products

     
            
       
