from bson import ObjectId
from typing import Any, Dict, Union, List
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo import MongoClient
from pymongo.client_session import ClientSession
from pymongo.results import InsertOneResult, UpdateResult

from app.models.models import OrderStub

class OrderRepository:
    def __init__(self, db: Database, client:MongoClient) -> None:
        self.db: Database = db
        self.orders: Collection = self.db['orders']
        self.client:MongoClient = client

    def create_order_stub(self, order: OrderStub, session:None|ClientSession = None) -> OrderStub:
        order_dict: Dict[str, Any] = order.model_dump()      
        retrived_id : str = order.id  
        if retrived_id:
            order_dict['_id'] = retrived_id
        order_dict.pop('id')

        insert_result: InsertOneResult = self.orders.insert_one(order_dict, session=session)
        order.id = str(insert_result.inserted_id)

        return order

    def update_order_stub_status_by_id(self, id:str, status:str, session: ClientSession) -> OrderStub | None:
        update_result: UpdateResult = self.orders.update_one(

        {"_id": ObjectId(id)},
        {"$set": {"status": status}},
        session=session)
        
        if update_result.matched_count == 1:
            updated_order = self.orders.find_one({"_id": ObjectId(id)})
            return updated_order
        return None
    
    def get_order_stub_by_id(self, id:str) -> OrderStub | None:
        found_order : Union[OrderStub, None] = self.orders.find_one({"_id": id})
        if not found_order:
            return None
        return OrderStub(**found_order)

     
            
       
