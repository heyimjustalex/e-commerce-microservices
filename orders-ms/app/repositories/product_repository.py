from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertOneResult
from app.models.models import Product,PyObjectId
from typing import Any, Dict, Union
from typing import List
from pymongo import MongoClient
from bson import ObjectId

class ProductRepository:
    def __init__(self, db: Database, client:MongoClient) -> None:
        self.db: Database = db
        self.products: Collection = self.db['products']
        self.client:MongoClient = client

    def create_product(self, product: Product) -> Product:
        product_dict: Dict[str, Any] = product.model_dump()
        if product_dict['id']:
            product_dict['_id'] = ObjectId(product_dict['id'])
            product_dict.pop('id') 
        id: InsertOneResult = self.products.insert_one(product_dict)
        product.id = str(id.inserted_id)
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
    
    def get_products_of_category(self, category_id:PyObjectId) -> Union[List[Product], None]:
        products_data = list(self.products.find({"categories": ObjectId(category_id)}))
        if not products_data:
            return None
        products: List[Product] = [Product(**data) for data in products_data]
        return products

     
            
       
