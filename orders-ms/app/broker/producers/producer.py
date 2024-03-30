
from fastapi import FastAPI, HTTPException
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
import json
from json.decoder import JSONDecodeError
from app.models.models import *
from app.models.models import ShopProductEvent
from app.repositories.order_repository import OrderRepository

class MessageProducer:
    def __init__(self) -> None:
        self.KAFKA_BOOTSTRAP_SERVERS:str = 'message-broker:19092'
        self.KAFKA_TOPIC:str = 'shop'
        self.KAFKA_GROUP:str = 'group'
        self.producer:AIOKafkaProducer | None = None

    def _serializer(self, message):
        return json.dumps(message).encode('utf-8')


    async def get_producer(self):
        producer = AIOKafkaProducer(
        value_serializer=self._serializer,
        bootstrap_servers=self.KAFKA_BOOTSTRAP_SERVERS,
        )
    
        await producer.start()
        return producer  
    
    async def shutdown_producer(self, producer: AIOKafkaProducer):
        await producer.stop()
   
