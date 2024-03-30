
from fastapi import FastAPI, HTTPException
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
import json
from json.decoder import JSONDecodeError
from app.models.models import *
from app.models.models import ShopProductEvent
from app.repositories.order_repository import OrderRepository

class MessageConsumer:
    def __init__(self, order_repository:OrderRepository) -> None:
        self.order_repository:OrderRepository = order_repository
        self.KAFKA_BOOTSTRAP_SERVERS:str = 'message-broker:19092'
        self.KAFKA_TOPIC:str = 'shop'
        self.KAFKA_GROUP:str = 'group'
        self.consumer: AIOKafkaConsumer | None = None

    def _deserializer(self,message):
        try:
            return json.loads(message.decode('utf-8'))
        except JSONDecodeError:
            if isinstance(message, bytes):
                return message.decode('utf-8')
            else:
                return message           

    async def get_consumer(self):
        if not self.consumer:
            self.consumer = AIOKafkaConsumer(self.KAFKA_TOPIC,
            value_deserializer=self._deserializer,
            bootstrap_servers=self.KAFKA_BOOTSTRAP_SERVERS,
             group_id=self.KAFKA_GROUP)
            await self.consumer.start()
        return self.consumer  
         
    async def shutdown_consumer(self,consumer:AIOKafkaConsumer):
        await consumer.stop()

 
    async def consume(self,consumer:AIOKafkaConsumer):
        try:
            async for message in consumer:
                print("consumed: ",  message.value)
                print("type: ",  type(message.value))
                if type(message.value) == dict:
                    json_mess = json.dumps(message.value)
                    if message.value['type'] == 'ProductCreate':
                        sent_id = message.value['product']['id']
                        message_fix: ShopProductEvent = ShopProductEvent.model_validate_json(json_mess)
                        message_fix.product.id= sent_id               
                        new_event : ShopProductEvent = ShopProductEvent(type=message_fix.type, product=message_fix.product)

                    print(new_event.model_dump())
        finally:    
            pass
        # await consumer.stop()    

