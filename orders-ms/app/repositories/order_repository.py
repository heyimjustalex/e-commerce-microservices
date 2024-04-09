from bson import ObjectId
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertOneResult
from app.models.models import Order, PyObjectId
from typing import Any, Dict, Union
from typing import List
from pymongo import MongoClient
from pymongo.client_session import ClientSession
from pymongo.results import InsertOneResult, UpdateResult

class OrderRepository:
    def __init__(self, db: Database, client:MongoClient) -> None:
        self.db: Database = db
        self.orders: Collection = self.db['orders']
        self.client:MongoClient = client

    def create_order(self, order: Order, session:None|ClientSession = None) -> Order:
        order_dict: Dict[str, Any] = order.model_dump()      
        order_dict.pop('id',None)
        
        insert_result: InsertOneResult = self.orders.insert_one(order_dict, session=session)
        order.id = str(insert_result.inserted_id)
        return order
 
    def get_orders_by_email(self,email:str) -> Union[List[Order],None]:
        orders_data = self.orders.find({"client_email": {"$regex": f"^{email}$", "$options": "i"}})
        if not orders_data:
            return None
        orders: List[Order] = [Order(**order_data) for order_data in orders_data]
        return orders

    def update_order_state_by_id(self, id:str, status:str, session: ClientSession) -> Order | None:
      
        update_result: UpdateResult = self.orders.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": status}},
        session=session        )
        
        if update_result.matched_count == 1:
            updated_order = self.orders.find_one({"_id": ObjectId(id)})
            print("UPDATE SUCCESS233", updated_order)
            return updated_order
        return None
            
    
     
            
       
