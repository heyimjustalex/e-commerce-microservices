from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertOneResult
from app.models.models import Product,ObjectIdStr
from typing import Any, Dict, Union
from typing import List
from bson import ObjectId
class ProductRepository:
    def __init__(self, db: Database) -> None:
        self.db: Database = db
        self.products: Collection = self.db['products']

    def create_product(self, product: Product) -> Product:
        product_dict: Dict[str, Any] = product.model_dump()
        id: InsertOneResult = self.products.insert_one(product_dict)
        product._id = id.inserted_id
        return product
    
    def get_products(self) -> List[Product]:
        products_data = list(self.products.find({}))  
        products: List[Product] = [Product(**data) for data in products_data]  
        return products    

    def get_product_by_name(self,name:str) -> Union[Product, None]:
        product: Union[Product, None]  = self.products.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
        if not product:
            return None
        return Product(**product)
    
    def get_products_of_category(self, category_id:ObjectIdStr) -> Union[List[Product], None]:

        products_data = list(self.products.find({"categories": ObjectId(category_id)}))

        if not products_data:
            return None
        products: List[Product] = [Product(**data) for data in products_data]
        return products

     
            
       
