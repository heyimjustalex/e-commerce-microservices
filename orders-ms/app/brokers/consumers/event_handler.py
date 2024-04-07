
from aiokafka import AIOKafkaProducer
from pydantic import BaseModel
from app.models.models import *
from app.repositories.product_repository import ProductRepository
from app.brokers.producers.producer import MessageProducer
from pymongo import MongoClient
from pymongo.client_session import ClientSession

class EventHandler:
    def __init__(self, product_repostiory:ProductRepository) -> None:
        self.product_repository: ProductRepository = product_repostiory
        self._producer:AIOKafkaProducer 
   
    def _construct_OrderStatusUpdateEvent(self, status:str, updated_bought_products:List[BoughtProduct]):
        status_uppercase :str = status.upper()
        orderStatusUpdateEvent:OrderStatusUpdateEvent = OrderStatusUpdateEvent(type="OrderStatusUpdate",status=status_uppercase,products=updated_bought_products) 
        return orderStatusUpdateEvent
    
    def _OrderStatusUpdateEvent_handler(self,event:OrderCreateEvent, session:ClientSession):
            determined_status :str = "ACCEPTED"
            products_with_updated_quantity : List[BoughtProduct] = []
            for product in event.order.products:                
                stocked_product : Product | None = self.product_repository.get_product_by_name(product.name)
                if not stocked_product:
                    determined_status = "REJECTED"
                    break
                stocked_quantity:int = stocked_product.quantity
                if product.quantity > stocked_quantity:
                    determined_status = "REJECTED"
                    break
                updated_product:Product | None=self.product_repository.update_product_quantity_by_name(product.name,product.quantity,session)
                if updated_product == None:
                    determined_status="REJECTED"
                    break
                else:
                    updated_product_stub : BoughtProduct = BoughtProduct(name=updated_product.name, price=updated_product.price, quantity=updated_product.quantity)
                    products_with_updated_quantity.append(updated_product_stub)
            return self._construct_OrderStatusUpdateEvent(determined_status,products_with_updated_quantity)      

    async def handleEvent(self,event:BaseModel):
        client:MongoClient = self.product_repository.get_mongo_client()
        self._producer = await MessageProducer.get_producer()
        if isinstance(event, OrderCreateEvent):            
            with client.start_session() as session:
                with session.start_transaction():
                    try:             
                        response_event:OrderStatusUpdateEvent = self._OrderStatusUpdateEvent_handler(event, session)
                        await self._producer.send(topic="shop",value=response_event.model_dump_json())
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