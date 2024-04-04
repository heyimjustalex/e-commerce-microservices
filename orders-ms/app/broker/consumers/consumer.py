
from aiokafka import AIOKafkaConsumer
import json
from json.decoder import JSONDecodeError
from ...models.models import Product
from app.models.models import *
from app.models.models import ProductCreateEvent
from app.repositories.product_repository import ProductRepository
import os

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
        print("ORDERS STARTUP CONSUMER")
        try:
            cls._consumer = AIOKafkaConsumer(
            cls.KAFKA_TOPIC,
            value_deserializer=cls._deserializer,
            bootstrap_servers=cls.KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='earliest',
            max_poll_records=100,
            enable_auto_commit=False,
            group_id=cls.KAFKA_GROUP)

            await cls._consumer.start()      
            cls.isStarted = True
            await cls._retrieve_messages()
          
        except:
            await cls._consumer.stop()
            cls.isStarted = False
  
        return cls._consumer
        
        
    @classmethod          
    async def shutdown_consumer(cls,consumer:AIOKafkaConsumer) -> None:
        await consumer.stop()
        cls.isStarted = False
    
    @classmethod
    async def consume(cls,consumer:AIOKafkaConsumer, product_repository:ProductRepository) -> None:
        print("Invoked consumer")
        try:
            async for message in consumer:
                print("IN MESSAGES")
                if type(message.value) == str:
                    json_mess = json.loads(message.value)
                    print("ORDER GOT MESS", json_mess)
                    if json_mess['type'] == 'ProductCreate':
                        sent_id = json_mess['product']['id']
                        message_fix: ProductCreateEvent = ProductCreateEvent.model_validate_json(message.value)
                        message_fix.product._id= sent_id           
                        message_fix.product.id= sent_id        
                        new_event : ProductCreateEvent = ProductCreateEvent(type=message_fix.type, product=message_fix.product)
                        existing_product: Product | None = product_repository.get_product_by_name(new_event.product.name)
                        if not existing_product:
                            print("not existing product", new_event.product.name)

                            prod: Product = product_repository.create_product(product=new_event.product)
                        else:
                            print("product exists, so im not creating")
        except Exception as e:
            print("ORDERSEXCEPTION: ProductCreate event consuming Error")
