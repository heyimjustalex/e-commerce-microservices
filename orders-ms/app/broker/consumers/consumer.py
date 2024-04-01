
from aiokafka import AIOKafkaConsumer
import json
from json.decoder import JSONDecodeError
from ...models.models import Product
from app.models.models import *
from app.models.models import ShopProductEvent
from app.repositories.product_repository import ProductRepository
from datetime import datetime

class MessageConsumer:
    KAFKA_BOOTSTRAP_SERVERS:str = 'message-broker:19092'
    KAFKA_TOPIC:str = 'shop'
    KAFKA_GROUP:str = 'group'
    _hasBeenLaunched = False
    _consumer : AIOKafkaConsumer
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
    async def startup_consumer(cls):
        cls._consumer = AIOKafkaConsumer(
        cls.KAFKA_TOPIC,
        value_deserializer=cls._deserializer,
        bootstrap_servers=cls.KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        max_poll_records=100,
        enable_auto_commit=False,
        group_id=cls.KAFKA_GROUP)

        await cls._consumer.start()
        for tp in cls._consumer.assignment():
           await cls._consumer.seek_to_beginning(tp)
       
        return cls._consumer
        
    @classmethod          
    async def shutdown_consumer(cls,consumer:AIOKafkaConsumer):
        await consumer.stop()
    
    @classmethod
    async def consume(cls,consumer:AIOKafkaConsumer, product_repository:ProductRepository):
        try:
            async for message in consumer:
                if type(message.value) == str:
                    json_mess = json.loads(message.value)
                    print("ORDER GOT MESS", json_mess)
                    if json_mess['type'] == 'ProductCreate':
                        sent_id = json_mess['product']['id']
                        message_fix: ShopProductEvent = ShopProductEvent.model_validate_json(message.value)
                        message_fix.product.id= sent_id               
                        new_event : ShopProductEvent = ShopProductEvent(type=message_fix.type, product=message_fix.product)
                        existing_product: Product | None = product_repository.get_product_by_name(new_event.product.name)
                        if not existing_product:
                            print("not existing product", new_event.product.name)
                            product_repository.create_product(product=new_event.product)
                  
        except Exception as e:
            print("ORDERSEXCEPTION: ProductCreate event consuming Error")

    # @classmethod
    # async def consume_when_launched(cls,consumer:AIOKafkaConsumer, product_repository:ProductRepository):

