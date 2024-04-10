
from aiokafka import AIOKafkaProducer
from pydantic import BaseModel

from app.models.models import *
from app.exceptions.definitions import *
from app.repositories.product_repository import ProductRepository
from app.repositories.order_repository import OrderRepository
from app.brokers.producers.producer import MessageProducer
from pymongo import MongoClient
from pymongo.client_session import ClientSession

class EventHandler:
    def __init__(self, product_repostiory:ProductRepository, order_repository:OrderRepository) -> None:
        self.product_repository: ProductRepository = product_repostiory
        self.order_repository : OrderRepository = order_repository
        self._producer:AIOKafkaProducer 
        
    def _construct_ProductsQuantityUpdate(self,updated_bought_products:List[ProductStub]):
        products_quantity_update_event:ProductsQuantityUpdateEvent = ProductsQuantityUpdateEvent(type="ProductsQuantityUpdate",products=updated_bought_products) 
        return  products_quantity_update_event
    
    def _construct_OrderStatusUpdateEvent(self, status:str,order_id:str):
        status_uppercase :str = status.upper()
        order_status_update_event:OrderStatusUpdateEvent = OrderStatusUpdateEvent(type="OrderStatusUpdate",order_id=order_id,status=status_uppercase) 
        return  order_status_update_event
    
    def _OrderStatusUpdateEvent_handler(self,event:OrderCreateEvent, session:ClientSession) -> tuple[OrderStatusUpdateEvent,ProductsQuantityUpdateEvent]:
            determined_status :str = "ACCEPTED"
            products_with_updated_quantity : List[ProductStub] = []
            for product in event.order.products:                             
                stocked_product : Product | None = self.product_repository.get_product_by_name(product.name)
                
                if not stocked_product:
                    determined_status = "REJECTED"
                    break
                stocked_quantity:int = stocked_product.quantity
                if product.quantity > stocked_quantity:
                    determined_status = "REJECTED"
                    break   
             
            if determined_status=="ACCEPTED":
                for product in event.order.products:
                    stocked_product : Product | None = self.product_repository.get_product_by_name(product.name)
                    updated_product:Product | None=self.product_repository.decrease_product_quantity_by_name(product.name,product.quantity,session)
                    if updated_product == None or stocked_product == None:
                        raise 
                    else:
                        updated_product_stub : ProductStub = ProductStub(name=updated_product.name, price=updated_product.price, quantity=stocked_product.quantity-product.quantity)                  
                        products_with_updated_quantity.append(updated_product_stub)
            
            self.order_repository.create_order_stub(OrderStub(_id=event.order.id,status=determined_status))
            order_status_update_event:OrderStatusUpdateEvent = self._construct_OrderStatusUpdateEvent(determined_status,event.order.id)      
            products_quantity_update_event:ProductsQuantityUpdateEvent = self._construct_ProductsQuantityUpdate(updated_bought_products=products_with_updated_quantity)
            return order_status_update_event, products_quantity_update_event
    
    def _check_order_existance(self, id:str) -> bool:
        order_stub : OrderStub | None = self.order_repository.get_order_stub_by_id(id)
        if not order_stub:
            return False
        return True          

    async def handleEvent(self,event:BaseModel):
        client:MongoClient = self.product_repository.get_mongo_client()
        self._producer = await MessageProducer.get_producer()
        if isinstance(event, OrderCreateEvent):    
            print("PRODUCTS-MS: Got OrderCreateEvent",event)           
            with client.start_session() as session:
                with session.start_transaction():
                    try:    
                        if self._check_order_existance(event.order.id):    
                            print("PRODUCTS-MS: order ", event.order.id, " already exists")
                            raise OrderAlreadyExists()

                        response_events:tuple[OrderStatusUpdateEvent,ProductsQuantityUpdateEvent] = self._OrderStatusUpdateEvent_handler(event, session)
                        # Publish events
                        print("PRODUCTS-MS: Publishing event: OrderStatusUpdateEvent ", response_events[1].model_dump_json())
                        await self._producer.send(topic="shop",value=response_events[0].model_dump_json())
                        
                        print("PRODUCTS-MS: Publishing event: ProductsQuantityUpdateEvent ", response_events[1].model_dump_json())
                        await self._producer.send(topic="shop",value=response_events[1].model_dump_json())
                        session.commit_transaction()   
                    except Exception as e:           
                        print("PRODUCTS-MS: Aborting transaction of OrderCreateEvent")       
                        session.abort_transaction()         


     