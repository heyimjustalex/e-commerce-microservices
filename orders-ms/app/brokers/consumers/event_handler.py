
from aiokafka import AIOKafkaProducer
from pydantic import BaseModel
from app.models.models import *
from app.repositories.product_repository import ProductRepository
from app.repositories.order_repository import OrderRepository
from app.brokers.producers.producer import MessageProducer
from pymongo import MongoClient
from pymongo.client_session import ClientSession

class EventHandler:
    def __init__(self, product_repostiory:ProductRepository, order_repository:OrderRepository) -> None:
        self.product_repository: ProductRepository = product_repostiory
        self.order_repository: OrderRepository = order_repository
        self._producer:AIOKafkaProducer 
   
     
    def _OrderStatusUpdateEvent_consume_handler(self,event:OrderStatusUpdateEvent, session:ClientSession):
            
            updated_order : Order | None = self.order_repository.update_order_state_by_id(event.orderId,event.status, session)
            for product in event.products: 
                updated_product:Product | None= self.product_repository.update_product_quantity_by_name(product.name,product.quantity,session)
               


    async def handleEvent(self,event:BaseModel):
        client:MongoClient = self.product_repository.get_mongo_client()
        self._producer = await MessageProducer.get_producer()
        if isinstance(event, OrderStatusUpdateEvent):            
            with client.start_session() as session:
                with session.start_transaction():
                    try:   
                        print("OrderStatusUpdate Before")          
                        self._OrderStatusUpdateEvent_consume_handler(event, session)
                        
                        
                        session.commit_transaction()   
                    except Exception as e:                  
                        session.abort_transaction()        

        elif isinstance(event, ProductCreateEvent):
            existing_product: Product | None = self.product_repository.get_product_by_name(event.product.name)
            if not existing_product:
                print("ProductCreateEvent: Product, not existing, so I'm adding", event.product.name)
                self.product_repository.create_product(product=event.product)
            else:
                print("ProductCreateEvent: Product existing, so I'm not adding")

        elif isinstance(event, OrderStatusUpdateEvent):
            # Default case or error handling
            pass