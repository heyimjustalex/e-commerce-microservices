from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertOneResult
from app.models.models import Product
from typing import Any, Dict, Union
from typing import List

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
        return list(self.products.find({}))

    def get_product_by_name(self,name:str) -> Union[Product, None]:
        product: Union[Product, None]  = self.products.find_one({"name": name})
        if not product:
            return None
        return Product(**product)
    

     
            
       
