
from aiokafka import AIOKafkaProducer
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.client_session import ClientSession

from app.models.models import *
from app.exceptions.definitions import ProductQuantityUpdateFailed, OrderStatusUpdateFailed
from app.repositories.product_repository import ProductRepository
from app.repositories.order_repository import OrderRepository
from app.brokers.producers.producer import MessageProducer

class EventHandler:
    def __init__(self, product_repostiory:ProductRepository, order_repository:OrderRepository) -> None:
        self.product_repository: ProductRepository = product_repostiory
        self.order_repository: OrderRepository = order_repository
        self._producer:AIOKafkaProducer 
        
    def _OrderStatusUpdateEvent_consume_handler(self,event:OrderStatusUpdateEvent, session:ClientSession):       
            updated_order : Order | None = self.order_repository.update_order_state_by_id(event.order_id,event.status, session)
            if not updated_order:
                raise OrderStatusUpdateFailed ()
            
    def _ProductQuantityUpdate_consume_handler(self,event:ProductsQuantityUpdateEvent, session:ClientSession):
        for product in event.products: 
            updated_product:ProductStub | None= self.product_repository.update_product_quantity_by_name(product.name,product.quantity,session)
            if not updated_product:
                raise ProductQuantityUpdateFailed()
                
    async def handleEvent(self,event:BaseModel):
        client:MongoClient = self.product_repository.get_mongo_client()
        self._producer = await MessageProducer.get_producer()
        if isinstance(event, OrderStatusUpdateEvent):      
            print("ORDER-MS: Got OrderStatusUpdateEvent",event)     
            with client.start_session() as session:
                with session.start_transaction():
                    try:   
                        self._OrderStatusUpdateEvent_consume_handler(event, session)                       
                        session.commit_transaction()   
                    except Exception as e:           
                        print("ORDERS-MS: Aborting transaction after consuming OrderStatusUpdateEvent")       
                        session.abort_transaction()        

        elif isinstance(event, ProductCreateEvent):
            existing_product: ProductStub | None = self.product_repository.get_product_by_name(event.product.name)
            # Mechanism for retrieving messages that have happend when the service was offline
            if not existing_product:
                print("ORDERS-MS: Got ProductCreateEvent -> Product non-existing, adding to local products document-db", event.product.name)
                self.product_repository.create_product(product=event.product)
            else:
                print("ORDERS-MS: Got ProductCreateEvent -> Product existing, not adding")

        elif isinstance(event, ProductsQuantityUpdateEvent):
            client:MongoClient = self.product_repository.get_mongo_client()
            with client.start_session() as session:
                with session.start_transaction():
                    print("ORDER-MS: Got ProductsQuantityUpdateEvent",event)
                    try:   
                        self._ProductQuantityUpdate_consume_handler(event, session)                       
                        session.commit_transaction()   
                    except Exception as e:           
                        print("ORDERS-MS: Aborting transaction after consuming ProductsQuantityUpdateEvent")       
                        session.abort_transaction()        

                   