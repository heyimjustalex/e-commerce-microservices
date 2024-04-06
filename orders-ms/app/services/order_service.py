
import re
from app.models.models import Product, OrderCreateEvent
from app.repositories.order_repository import OrderRepository
from app.schemas.schemas import OrderCreateRequest, OrdersRequest
from app.exceptions.definitions import BrokerMessagePublishError,OrderPlacingFailed, ProductQuantityBad, InvalidTokenEmail, ProductNotFound,OrdersIncorrectFormat, OrdersNotFound,CategoryNotFound, ProductNotFound, ProductAlreadyExists, ProductIncorrectFormat
from typing import Union, List, Tuple, Any
from app.models.models import Order, PyObjectId, BuyProductItem
from app.repositories.product_repository import ProductRepository
from pymongo import MongoClient
from app.broker.producers.producer import MessageProducer
from aiokafka import AIOKafkaProducer


class OrderService:
    def __init__(self, order_repository: OrderRepository, product_repository:ProductRepository) -> None:
        self.order_repository: OrderRepository = order_repository
        self.product_repository: ProductRepository = product_repository
        
    def _verify_create_request_format(self, data: OrderCreateRequest) -> None:
        bought_products: List[BuyProductItem] = data.products

        if bought_products is None :
           raise OrdersIncorrectFormat()
        if data.email is None :
            raise InvalidTokenEmail()

        for product in bought_products:
            if product is None:
                raise OrdersIncorrectFormat()
            if not isinstance(product, BuyProductItem):
                raise OrdersIncorrectFormat()
            if not isinstance(product.name, str) or not re.match(r'^[a-zA-Z0-9\s]+$', product.name):
                raise OrdersIncorrectFormat()
            if not isinstance(product.quantity, int) or product.quantity <= 0:
                raise OrdersIncorrectFormat()

    def get_orders_by_email(self, email:str) -> List[Order]: 
        orders: Union[List[Order],None] = self.order_repository.get_orders_by_email(email)        
        if not orders:
            raise OrdersNotFound()
        return orders   
    
    def _calculate_order_cost(self, products:List[BuyProductItem])->float:
        order_cost:float = 0
        for product in products:
            prod_got_by_name: Product | None = self.product_repository.get_product_by_name(product.name)
            if not prod_got_by_name:
                raise ProductNotFound()
            order_cost+=prod_got_by_name.price * product.quantity
            product.price = prod_got_by_name.price
        return order_cost
    
    def _check_products_existance_and_quantity(self,products:List[BuyProductItem]):
        for product in products:
            prod_got_by_name: Product | None = self.product_repository.get_product_by_name(product.name)
            if not prod_got_by_name:
                raise ProductNotFound()
                      
            if prod_got_by_name.quantity < product.quantity:
                raise ProductQuantityBad()

    async def _publish_OrderCreateEvent_to_broker(self,order:Order) -> None:                    
        try:
            create_order_event : OrderCreateEvent = OrderCreateEvent(type="OrderCreate", order=order)
            message_producer: AIOKafkaProducer = await MessageProducer.get_producer()
            await message_producer.send(topic='shop', value=create_order_event.model_dump_json())                
            print("ORDERS-MS SENT MESSAGE", create_order_event.model_dump_json())
        except:
            raise BrokerMessagePublishError()

    async def create_order_with_event_OrderCreate(self, data:OrderCreateRequest) -> Order:
       
        self._verify_create_request_format(data)             
       
        email : str = data.email
        #Bought product
        products: List[BuyProductItem] = [BuyProductItem(name=product.name.lower(), price=product.price, quantity=product.quantity) for product in data.products]  
        self._check_products_existance_and_quantity(products)
        order_cost:float = self._calculate_order_cost(products)  
        order : Order = Order(client_email=email.lower(),cost=order_cost, status="PENDING", products=products)

        client:MongoClient = self.product_repository.get_mongo_client()
        with client.start_session() as session:
            with session.start_transaction():
                try:
                    created_order: Order = self.order_repository.create_order(order, session)
                    # await self._publish_OrderCreateEvent_to_broker(created_order)
          
                except Exception as e:
                    session.abort_transaction()   
                    raise OrderPlacingFailed()       

        return created_order

