from fastapi import FastAPI, HTTPException
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
import json
from json.decoder import JSONDecodeError
from app.models.models import *
from app.models.models import ShopProductEvent
from pydantic import BaseModel

class MessageProducer:
    KAFKA_TOPIC:str = 'shop'
    KAFKA_GROUP:str = 'group'
    def __init__(self) -> None:
        self.KAFKA_BOOTSTRAP_SERVERS:str = 'message-broker:19092'
        self.isStarted = False
       
    async def get_producer(self):  
        if not self.isStarted:
            self._producer: AIOKafkaProducer = await self._create_producer()
            self.isStarted = True
        return self._producer  

    async def _create_producer(self):
        producer = AIOKafkaProducer(
            value_serializer=self._serializer,        
            bootstrap_servers=self.KAFKA_BOOTSTRAP_SERVERS,
        )
        await producer.start()
        return producer
        
    async def shutdown_producer(self):
        if self.isStarted:
            await self._producer.stop()

    def _serializer(self, message):
        test: bytes = json.dumps(message).encode('utf-8')
        return test
