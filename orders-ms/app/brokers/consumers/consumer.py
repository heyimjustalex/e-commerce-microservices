
from aiokafka import AIOKafkaConsumer
import json
from json.decoder import JSONDecodeError
from app.models.models import Product
from app.models.models import *
from app.models.models import ProductCreateEvent
from app.repositories.product_repository import ProductRepository
import os
import traceback
from app.brokers.consumers.event_handler import EventHandler
class MessageConsumer:
  
    KAFKA_TOPIC:str  = os.getenv('KAFKA_TOPIC', 'shop')
    KAFKA_GROUP:str =  os.getenv('KAFKA_GROUP', 'group')
    KAFKA_BOOTSTRAP_SERVERS:str = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'message-broker:19092')
    isStarted = False
    _consumer : AIOKafkaConsumer

    @classmethod   
    async def get_consumer(cls) -> AIOKafkaConsumer:  
        if not cls.isStarted:
            cls._consumer: AIOKafkaConsumer 
            cls.isStarted = True
        return cls._consumer
    
    @classmethod
    def _deserializer(cls,message):
        try:
            return json.loads(message.decode('utf-8'))
        except JSONDecodeError:
            if isinstance(message, bytes):
                return message.decode('utf-8')
            else:
                return message       

    @classmethod
    async def _retrieve_messages(cls) -> None:
        for tp in cls._consumer.assignment():
           await cls._consumer.seek_to_beginning(tp)    

    @classmethod
    async def startup_consumer(cls) -> AIOKafkaConsumer:
        try:
            cls._consumer = AIOKafkaConsumer(          
            cls.KAFKA_TOPIC,
            value_deserializer=cls._deserializer,
            bootstrap_servers=cls.KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='earliest',
            max_poll_records=100,
            enable_auto_commit=False,
            group_id=cls.KAFKA_GROUP)  
            cls.isStarted = True  
          
        except:
            await cls._consumer.stop()
            cls.isStarted = False
  
        return cls._consumer
        
        
    @classmethod          
    async def shutdown_consumer(cls,consumer:AIOKafkaConsumer) -> None:
        await consumer.stop()
        cls.isStarted = False
    
    @classmethod
    async def consume(cls, product_repository:ProductRepository) -> None:
        while True:           
            try:
                await cls.startup_consumer()
                await cls._consumer.start()
                await cls._retrieve_messages()
                event_handler:EventHandler=EventHandler(product_repostiory=product_repository) 
                async for message in cls._consumer:  
                    if type(message.value) == str:
                        json_mess = json.loads(message.value)

                        if json_mess['type'] == 'ProductCreate':                           
                            sent_id = json_mess['product']['id']
                            product_create_event: ProductCreateEvent = ProductCreateEvent.model_validate_json(message.value)
                            product_create_event.product._id= sent_id           
                            product_create_event.product.id= sent_id       
                            await event_handler.handleEvent(product_create_event)
                        elif json_mess['type'] == 'OrderStatusUpdate':                
                            print("VALUE",message.value)            
                            order_status_update_event: OrderStatusUpdateEvent = OrderStatusUpdateEvent.model_validate_json(message.value)
                            print(order_status_update_event)


            except Exception as e:
                await cls._consumer.stop()
                print("ORDERSEXCE PTION: ProductCreate event consuming Error", traceback.print_exc())
                