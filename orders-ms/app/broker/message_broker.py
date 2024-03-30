
from fastapi import FastAPI, HTTPException
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
import json
from json.decoder import JSONDecodeError
from app.models.models import *
from app.models.models import ShopProductEvent


class MessageBroker:
    KAFKA_BOOTSTRAP_SERVERS:str = 'message-broker:19092'
    KAFKA_TOPIC:str = 'shop'
    KAFKA_GROUP:str = 'group'   

    @classmethod
    def _serializer(cls, message):
        return json.dumps(message).encode('utf-8')
    
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
        consumer = AIOKafkaConsumer(
        cls.KAFKA_TOPIC,
        value_deserializer=cls._deserializer,
        bootstrap_servers=cls.KAFKA_BOOTSTRAP_SERVERS,
        group_id=cls.KAFKA_GROUP)
        await consumer.start()
        return consumer
    
    @classmethod
    async def startup_producer(cls):
        producer = AIOKafkaProducer(
        value_serializer=cls._serializer,
        bootstrap_servers=cls.KAFKA_BOOTSTRAP_SERVERS,
        )
    
        await producer.start()
        return producer
    
    @classmethod          
    async def shutdown_consumer(cls,consumer:AIOKafkaConsumer):
        await consumer.stop()

    @classmethod  
    async def shutdown_producer(cls, producer: AIOKafkaProducer):
        await producer.stop()
    
    @classmethod
    async def consume(cls,consumer:AIOKafkaConsumer):
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

