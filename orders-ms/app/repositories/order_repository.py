from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertOneResult
from app.models.models import Order, PyObjectId
from typing import Any, Dict, Union
from typing import List
from pymongo import MongoClient

class OrderRepository:
    def __init__(self, db: Database, client:MongoClient) -> None:
        self.db: Database = db
        self.orders: Collection = self.db['orders']
        self.client:MongoClient = client

    def create_order(self, order: Order) -> Order:
        order_dict: Dict[str, Any] = order.model_dump()
        id: InsertOneResult = self.orders.insert_one(order_dict)
        order._id = id.inserted_id
        return order
 
    def get_orders_by_email(self,email:str) -> Union[List[Order],None]:
        orders_data = self.orders.find({"client_email": {"$regex": f"^{email}$", "$options": "i"}})
        if not orders_data:
            return None
        orders: List[Order] = [Order(**order_data) for order_data in orders_data]
        return orders

    

     
            
       
